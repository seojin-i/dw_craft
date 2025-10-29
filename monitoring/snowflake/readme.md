Snowflake Operation과 관련된 작업

- CodeBuild는 "자동 Build, Transform 단계"를 담당하는 AWS 서비스 입니다. 
- CloudFormation은 "AWS Resource를 자동으로 만들어주는 Iac를 위한 도구 입니다. 

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
  - AWS Glue을 자동으로 실행하기 위한 Iac. 
5. glue-notebook.buildSpec.yaml
   - AWS CodeBuild의 Build Spec을 정의한 파일 (CodeBuild가 어떤것을 빌드할지를 정의한 스크립트)
   - Jupyter Notebook file을 Python file로 변환(.ipynb -> .py) 후 AWS Glue용 Script로 만들고 s3에 Upload
   - 추후 Glue Job은 s3에 Upload된 파일을 참조하여 실행되는 구조이다.
     - 최종 결과물:
          - build-glue-job-script.py
          - stack-template.yaml
6. glue-scheduled-job-stack-templates.yaml
   - AWS Glue Job을 정해진 Scheduled에 맞춰 자동으로 실행시키도록 만들기 위한 CloudFormation Iac.
7. glue-script.buildSpec.yaml
   - 실제로 Glue Job을 실행하기 위한 Script
   - s3 경로의 파일을 참조하여 최종적으로 Glue Job에 전달할 Parameter를 포함한 최종 배포용 .yaml 파일을 생성한다.
8. create_mart.sql
   - 게임 통계에 대한 사용자의 요구사항을 반영한 Mart를 개발한 작업 Sample
9. Sensitive_data_Masking.sql
   - 민감 정보 Masking 처리와 관련된 Masking Policy 개발 
