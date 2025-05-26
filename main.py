import streamlit as st
from Modules.ModuleImport import *  # 모든 모듈을 불러옵니다.
from Modules.VectorStore import *
load_dotenv()
from Modules.prompt import contextual_prompt
from Modules.prompt import translate_template1
from Modules.prompt import summary_prompt
from Modules.prompt import image_prompt_template
from Modules.ContextToPrompt import ContextToPromptㅋ
from Modules.RetrieverWrapper import RetrieverWrapper
import Modules.Speech as Speech
from pages.chatbot_main import chatbot_main
from pages.image_main import image_main
from streamlit_option_menu import option_menu

def init():
    # 경로가 없으면 생성
    if not os.path.exists("History"):
        os.makedirs("History")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    if "messages" not in st.session_state:  # 입력값에 대한 메시지
        st.session_state["messages"] = []
    if "active" not in st.session_state:    # 선택한 대화방
        st.session_state["active"] = ""
    if "side_data" not in st.session_state: # 사이드바에 표시하기위한 데이터
        st.session_state["side_data"] = []
    if 'rerun' not in st.session_state:
        st.session_state["rerun"] = False
    if 'menu' not in st.session_state:
        st.session_state["menu"] = ""

st.markdown(
    """
    <style>
        div[data-testid="stToolbar"] {
            display:none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("🚘 과시리")

# 사이드바
with st.sidebar:
    def on_change(key):
        st.session_state["menu"] = key

    selected = option_menu(None, ["Home", 'Image'], 
        icons=['house', 'camera'], menu_icon="cast", key="menu_key", default_index=0, on_change=on_change)
init()

menu_dict = {
    "Home" : {"fn": chatbot_main},
    "Image" : {"fn": image_main},
}
if 'menu_key' in st.session_state and st.session_state["menu_key"]:
    menu_dict[st.session_state["menu_key"]]["fn"]()
else:
    chatbot_main()    
