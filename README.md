# 특허 판사 챗봇 (특허 관련 챗봇)

## 🏃‍♂️ 실행 가이드
```sh
git clone https://github.com/anem1c/TrafficAccident-Judge-LLM.git

cd TrafficAccident-Judge-LLM

pip install -r requirements.txt
```

```sh
streamlit run main.py
```

## 📈 프로젝트 진행 요약 및 업데이트 사항
* 1. Code text Modules, pages, main edit file
* 2. Edit the error code related to loading the OpenAI API.
* 3. Code to convert HTML URLs and to retrieve links and buttons during crawling, and edit text.
* 4. Cawrling sacn page error edit.


## 🥅 트러블 슈팅
* 음성 재생중 새로고침시 재생중인 음성이 중지되게 하고 싶었지만 streamlit lifecycle 추적 방법을 찾지못함
* rag 체인에 모델 입력까지 넣을 때 stream 형식으로 보여줄 수 없는 문제
* rag 체인 형식을 수정해 모델 입력은 따로 받아 stream으로 진행 가능하도록 수정 


