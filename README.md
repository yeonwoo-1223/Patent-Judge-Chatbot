# 상표 이미지 유사도 확인

## 크롤링 방법
- 공공데이터포털의 OPENAPI KEY를 발급 받아 상표 검색 URL과 함께 사용
- 크롤링으로 출원 번호를 txt 파일로 저장하고, 저장한 txt 파일을 기반으로 train 파일에 이미지 저장

## 이미지 유사도 확인
- ReNet 사용
- train 파일 내 상표 150장의 이미지를 기반으로 사용자가 입력한 사진과 유사도 비교
- 추후 사진 더 추가 예정

## 참고 GitHub 저장소
**sohnjunior / Patent-Attorney**
https://github.com/sohnjunior/Patent-Attorney
