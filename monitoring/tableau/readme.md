*Tableau Views Health Checker*
- 목적: 모든 Project의 모든 Workbooks의 모든 Views에 대해서 Health Check를 진행하기 위한 코드
- 구현 방식: AWS Lambda
- language: node.js
- File 설명
  - Tableu-Health-Check.yaml: Lambda에서 실행된 Service가 필요로하는 권한 및 설정들을 Iac로 표현
  - index.js: 실제 AWS Lambda에서 수행될 node.js 파일
  - package-lock.json, - package.json: node.js파일에서 서비스 구동시 필요한 여러가지 packages 정보
