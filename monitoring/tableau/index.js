const {Secrets} = require('nsus/secrets');
const {Tableau} = require('nsus/tableau/method');
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');  // aws-sdk V3
const xml2json = require('nsus/parser/xmltojson');
const process = require('process');
const axios = require('axios');

// 전역 변수 설정
let tableau;
const projectNameList = [];                      // DX 프로젝트 하위에 존재하는 모든 project_id가 담긴 list
const workbookIdDict = {};                         // Project에 존재하는 모든 workbook List
const viewIdDict = {};                             // Workbook에 존재하는 모든 View List
const errorList = [];                           // Slack 결과로 반활될 Error가 있는 Tableau View List
const secretName = 'prod/slack/webhook_url';    // SecretManager Name
const region = 'ap-east-1';                     // region

// lambda Handler
exports.handler = async (event) => {
    try {
        // 전역 변수에 tableau 객체를 전달.
        tableau = await getTableauInfo();
        await tableauSignIn();

        // DX 프로젝트에 존재하는 모든 project name을 알기 위해 가장 먼저 수행되어야 하는 함수.
        await recursiveGetAllProjectId({projectId: process.env.TABLEAU_DX_PROJECT_ID});  // 최상위 DX Project id

        // project name을 통해서 해당 프로젝트에 존재하는 모든 workbook id가져와서 list에 저장.
        await getAllWorkbookId();

        // 위 workbook id를 통해서 해당 workbook에 존재하는 모든 view list 정보 저장.
        await getAllViewId();

        // 모든 View에 api call을 통해서 데이터 존재 여부를 확인.
        await getViewData();

        // Slack Webhook Url 정보를 SecretManager에서 가져온다.
        const slackWebhookUrl = await getSecretInfo();

        // 최종적으로 Slack Message로 결과를 전달한다.
        await sendSlackMessage(slackWebhookUrl);

    } catch (error) {
        console.error(error);
        throw error;
    }
};

async function getSecretInfo(){
    const client = new SecretsManagerClient({ region: region });
    const command = new GetSecretValueCommand({ SecretId: secretName });
    const data = await client.send(command);
    const slackWebhookUrl = JSON.parse(data.SecretString)['notice-data_warehouse'];
    return slackWebhookUrl;
}

async function getTableauInfo() {
    const tableauInfo = await Secrets.getSecrets({
        secretName: 'tableau', region: 'ap-east-1', env: 'prod'
    });

    const tableau = await new Tableau({
        baseUrl: process.env.TABLEAU_BASE_URL,
        siteId: process.env.TABLEAU_SITE_ID,
        patName: tableauInfo.pat_name,
        patSecret: tableauInfo.pat_secret,
        siteName: process.env.TABLEAU_SITE_NAME
    });
    return tableau;
}

async function tableauSignIn() {
    try {
        const res = await tableau.httpClient.post(`/api/${tableau.apiVersion}/auth/signin`, tableau.signinParam);
        tableau.token = (await xml2json(res.data)).tsResponse.credentials[0].$.token;
        tableau.httpClient.defaults.headers.common['X-Tableau-Auth'] = tableau.token;
    } catch (err) {
        console.log('tableauSignIn() Error: ', err);
        throw err;
    }
}

/*
1. 제일 먼저 실행되어야 하는 함수.
   재귀형로 동작되며, 가장 최상위 프로젝트(DX)에 존재하는 모든 project name을 찾아서 list에 저장.
 */
async function recursiveGetAllProjectId({projectId}) {
    try {
        const projectInfoData = await getDataFromTableauApi(`/api/3.4/sites/${tableau.siteId}/projects?filter=parentProjectId:eq:${projectId}`);
        const jsonData = await xml2json(projectInfoData); // json 형태로 변환한 데이터
        const projectList = jsonData.tsResponse.projects[0].project;

        // Project 정보에서 Id값만 추출하여 list에 저장.
        if (projectList && projectList.length !== 0) {
            for (const item of projectList) {
                projectNameList.push(item.$.name);
                await recursiveGetAllProjectId({projectId: item.$.id});
            }
        }
        console.log('1번째 함수 완료 ');
    } catch (error) {
        console.log('recursiveGetAllProjectId() Error: ', error);
        throw error;
    }
}

/*
2. 두번째로 실행 되어야 할 함수.
   모든 Project에 존재하는 workbook_id 를 가져와서 list에 저장.
   Workbook의 경우 tableau api가 특정 workbook id를 통해서 하위 view list를 가져오는 api를 제공하기 때문에 id값을 추출.
 */
async function getAllWorkbookId() {
    try {
        for (const project_name of projectNameList) {
            const workBookInfoData = await getDataFromTableauApi(`/api/3.4/sites/${tableau.siteId}/workbooks?filter=projectName:eq:${project_name}`);
            const jsonData = await xml2json(workBookInfoData);
            const workbookList = jsonData.tsResponse.workbooks[0].workbook; // jsonData.tsResponse.workbook[0].$.webpageUrl

            // Workbook 정보에서 Id값 만 추출 하여 저장.
            if (workbookList && workbookList.length !== 0) {
                for (const item of workbookList) {
                    workbookIdDict[item.$.id] = {};
                    workbookIdDict[item.$.id]['workbook_name'] = item.$.name;
                    workbookIdDict[item.$.id]['workbook_url'] = item.$.webpageUrl;
                }
            } else {
                console.log(`${project_name} 프로젝트에는 Workbook이 존재하지 않습니다.`);
            }
        }
        console.log('2번째 함수 완료 ');
    } catch (error) {
        console.log('getAllWorkbookId() Error: ', error.message);
        throw error;
    }
}

/*
3. 세번재로 실행되는 함수.
   workbook id를 이용하여, 해당 workbook에 존재하는 모든 view id를 저장.
 */
async function getAllViewId() {
    try {
        for (const workbook_id in workbookIdDict) {
            const viewInfoData = await getDataFromTableauApi(`/api/3.4/sites/${tableau.siteId}/workbooks/${workbook_id}/views`);
            const jsonData = await xml2json(viewInfoData);
            const viewList = jsonData.tsResponse.views[0].view;

            // View 정보에서 Id값 만 추출 하여 저장.
            if (viewList && viewList.length !== 0) {
                for (const item of viewList) {
                    viewIdDict[item.$.id] = {};
                    viewIdDict[item.$.id]['view_name'] = item.$.name;
                    viewIdDict[item.$.id]['workbook_id'] = workbook_id;
                }
            } else {
                console.log(`${viewList.item.$.name} Workbook에는 View가 존재하지 않습니다.`);
            }
        }
        console.log('3번째 함수 완료 ');
    } catch (error) {
        console.log('getAllViewId() Error: ', error.message);
        throw error;
    }
}

/*
4. 네번째로 수행되는 함수
View id를 통해 모든 View에 api call하여 Data 존재여부 확인. ViewData가 존재하지 않거나, Index 필드의 값이 1이하인 경우, Api call status가 400, 401인 경우 Error로 판단.
    - Api Call Filter: ?vf_Field%20Name=Value
                        - vf_: Tableau filtering 조건으로 작성될 FieldName의 Prefix 예약어
                        - %20: FieldName에 공백이 존재할 경우, 공백이 있다는 것을 알리기 위한 Tableau 예약어
                        - =Value: FieldName의 조건으로 지정될 값을 의미.
2024-02-14 추가된 내용
    - 정상적인 View임에도 불구하고 Api Call시 Authentication Token 만료로 인해 401 error가 발생하는 이슈 존재.
        - 해결방법
            - Tableau Document에도 api call을 통해 받아오는 Authentication Token에 대한 expired time에 대한 가이드가 존재하지 않아 정확한 토큰 만료 시간을 알 수 없음.
              따라서 Api call시 401 Status code가 발생할 경우 Tableau 인증 토큰을 새로 받아와서 에러가 발생한 View부터 다시 call 하도록 코드 수정.
              - 400인 경우: errorList에 해당 뷰 정보를 넣는다.
              - 401인 경우: List형태로 api 결과 값을 받아온 뒤, api 인증 토큰을 새로 받아서 api call 재시도.
 */
async function getViewData() {
    try {
        for (const view_id in viewIdDict) {
            const viewData = await getViewDataFromTableauApi(`/api/3.4/sites/${tableau.siteId}/views/${view_id}/data?vf_Index=1`);
            console.log('===============================================');
            console.log(viewData);
            if (!viewData || (viewData && viewData.length <= 1) || (viewData == 400)){
                errorList.push(viewIdDict[view_id]);    // Error가 있는 view의 Name을 list에 저장함.
                console.log('error view_1: ', viewIdDict[view_id]);
            }
            else if(Array.isArray(viewData)){   // error status가 401인 경우 값을 List 형태로 전달 받게 된다.
                await tableauSignIn();
                for (const api of viewData[1]){
                    const viewData = await getViewDataFromTableauApi(api);
                    if (!viewData || (viewData && viewData.length <= 1)){
                        errorList.push(viewIdDict[view_id]);
                        console.log('error view_2: ', viewIdDict[view_id]);
                    }
                }
            }
        }
        console.log('4번째 함수 완료 ');
    } catch (error) {
        console.error('getViewData() Error:', error.message);
        throw error;
    }
}

// 각 Tableau Api를 호출할 때 공통적으로 사용될 Function.
async function getDataFromTableauApi(ApiUrl) {
    try {
        if (!tableau.token) {
            await tableauSignIn();
        }
        const response = await tableau.httpClient.get(ApiUrl);
        if (response.data) {
            return response.data;
        }
    } catch (error) {
        console.error('getDataFromTableauApi() Error: ', error.message);
        console.log('error.response.status: ', error.response.status);
        return error.response.status;
    }
}

// ViewData를 가져올 때만 사용할 Function
async function getViewDataFromTableauApi(ApiUrl) {
    const errorApiUrlList = [];
    try {
        if (!tableau.token) {
            await tableauSignIn();
        }
        const response = await tableau.httpClient.get(ApiUrl);
        if (response.data) {
            return response.data;
        }
    } catch (error) {
        console.error('getDataFromTableauApi() Error: ', error.message);
        console.log('error.response.status: ', error.response.status);
        if (error.response.status == 400){      // error 코드가 400인 경우 error code를 그대로 전달 하고,
            return error.response.status;
        }
        else if(error.response.status == 401){  // error 코드가 401인 경우 [error_code, ApiUrl] 을 전달 한다.
            errorApiUrlList.push(ApiUrl);
            return [error.response.status, errorApiUrlList];
        }
    }
    console.log("errorApiUrlList : ", errorApiUrlList);
}

// Slack Error List가 존재할 경우 Block에 추가될 Section을 생성하기 위한 function.
function makeSlackBlock({text}) {
    const addBlock = {
        "type": "section", "text": {
            "type": "mrkdwn", "text": `${text}`
        }
    };
    return addBlock;
}

// Slack 으로 Tableau Health Check Result를 전달하기 위한 Function.
async function sendSlackMessage(webhookUrl) {
    try {
        const urlList = [];
        const slackMessageTemplate = {
            channel: 'notice-data_warehouse', username: 'Tableau', text: `Tableau Views Health Check`, blocks: [{
                "type": "header", "text": {
                    "type": "plain_text", "text": "Tableau Views Health Check", "emoji": true
                }
            }, {
                "type": "section", "text": {
                    "type": "plain_text", "text": "", "emoji": true
                }
            }]
        };

        //  Result View: Test를 위해서 임시로 생성된 뷰로 예외처리, Session Transaction: PH 런칭전까지 결과 없음으로 1/12까지 잠정 예외 처리.
        const filteredList = errorList.filter(error => error.view_name !== 'Empty Result View for Test (Don\'t Mind This)' && error.view_name !== 'Session Transaction Report');

        // Error list가 존재할 경우 blocks 부분을 추가한다.
        if (filteredList.length !== 0) {
            const errorMsg = `Failed:\n`;
            slackMessageTemplate["blocks"][1].text.text = errorMsg;
            for (const viewInfo of filteredList) {
                const workbookId = viewInfo['workbook_id'];                                                         // 해당 View가 속한 workbook id를 가져 온다.
                const workbookUrl = workbookIdDict[workbookId]['workbook_url'];                                     // workbook의 URL을 가져온다.
                urlList.push(`<${workbookUrl}|${workbookIdDict[workbookId]['workbook_name']} / ${viewInfo['view_name']}>\n`);
            }
            const addBlock = makeSlackBlock({text: urlList.join('')});
            slackMessageTemplate["blocks"].push(addBlock);
        } else {
            const errorMsg = 'Succeeded';
            slackMessageTemplate["blocks"][1].text.text = errorMsg;
        }

        const response = await axios.post(webhookUrl, slackMessageTemplate);

        if (response.statusCode === 200) {
            console.log('Slack으로 메세지를 성공적으로 전달 하였습니다. ', JSON.stringify(response.data));
        }
    } catch (error) {
        console.error('sendSlackMessage() Error: ', error);
        throw error;
    }
}
