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
  - AWS Glue에서 정해진 시간마다 자동으로 실행되는 Scheduled 작업을 자동으로 실행하기 위한 Iac. 
5. glue-notebook.buildSpec.yaml
   - AWS CodeBuild의 Build Spec을 정의한 파일 (CodeBuild가 어떤것을 빌드할지를 정의한 스크립트)
   - Jupyter Notebook file을 Python file로 변환(.ipynb -> .py) 후 AWS Glue용 Script로 만들고 s3에 Upload
   - 추후 Glue Job은 s3에 Upload된 파일을 참조하여 실행되는 구조이다.
     - 최종 결과물:
          - built-glue-job-script.py
          - stack-template.yaml
6. glue-scheduled-job-stack-templates.yaml
   - 
7. glue-script.buildSpec.yaml
   - 
