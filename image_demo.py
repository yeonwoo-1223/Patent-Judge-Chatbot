import streamlit as st
import streamlit as st
from Modules.ModuleImport import *  # 모든 모듈을 불러옵니다.
from Modules.VectorStore import *
load_dotenv()
from Modules.prompt import image_prompt_template
from Modules.ImageDetect import get_image_input

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
now_dir = os.getcwd()
translate_model = ChatOpenAI(model="gpt-4o-mini")

def image():
    # 이미지 업로드
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        print(f"챗봇 이미지 세션 스테이트 : ",st.session_state["messages"])
        # 기본 메시지 화면에 표시
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])


        image_query,image = get_image_input(uploaded_file)
        if(image_query == ''): # 이미지를 인식할 수 없을 때
            with st.chat_message("assistant"):
                response = st.warning(
                    "죄송합니다. 이미지를 인식할 수 없습니다. 다른 이미지로 시도해주세요."
                )

        else:
            # 사용자 메시지 표시
            with st.chat_message("user"):  
                st.write("위 이미지에 대해서 설명해줘.")
            st.image(image, caption="감지된 결과", use_container_width=True)
            # AI 응답 처리
            with st.chat_message("assistant"):
                
                # 이미지에 대한 파손 부위 분석을 위한 프롬프트 생성
                prompt = image_prompt_template.format_messages(content=image_query)
                # AI 모델에 대한 응답 요청 (ChatOpenAI 모델 사용)
                response = translate_model.invoke(prompt)
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages = [
                        *[
                            {"role": "system", "content":response.content}
                        ],
                    ],
                    stream = True,
                )
                response = st.write_stream(stream)
