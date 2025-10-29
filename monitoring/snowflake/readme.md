Snowflake Operation과 관련된 작업
1. glue-code-pipeline-templates.yaml
   - AWS Glue를 CloudFormation Template화 한 파일. (자동으로 Build 하기 위해 정의해둔 Iac)
   - AWS CodeBuild를 사용하여 AWS Glue 작업이 수행되도록 한다.
     - Source 단계
          - Github에서 코드를 가져온다.
     - Build 단계
          - AWS CodeBuild로 코드를 Build 한다.
     - Deploy 단계
          - AWS CloudFormation을 통해 Glue Job 생성 + Update.
3. glue-job-templates.yaml
4. glue-notebook.buildSpec.yaml
   - AWS Glue를 Jupyter Notebook으로 Local Test 해보기 위한 Iac
5. glue-scheduled-job-stack-templates.yaml
6. glue-script.buildSpec.yaml
