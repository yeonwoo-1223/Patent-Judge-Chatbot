import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# ✅ 1. .env 파일 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# ✅ 2. API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

# ✅ 3. 불러온 키 출력 (검증용, 나중에 삭제해도 됨)
print("🔐 OPENAI_API_KEY 불러오기 성공:", api_key[:8] + "..." if api_key else "키 없음")

# ✅ 4. 임베딩 객체 생성 (반드시 키 전달)
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=api_key  # ← 이 한 줄이 없으면 계속 에러남
)

# ✅ 5. FAISS 벡터스토어 로드
vector_store_law = FAISS.load_local(
    "Resources/vector_store_law", embeddings, allow_dangerous_deserialization=True)

vector_store_situation = FAISS.load_local(
    "Resources/vector_store_situation", embeddings, allow_dangerous_deserialization=True)

vector_store_rate = FAISS.load_local(
    "Resources/vector_store_rate", embeddings, allow_dangerous_deserialization=True)

# ✅ 6. 리트리버 정의
retriever = vector_store_law.as_retriever(
    search_type="similarity", search_kwargs={"k": 5})
retriever1 = vector_store_situation.as_retriever(
    search_type="similarity", search_kwargs={"k": 1})
retriever2 = vector_store_rate.as_retriever(
    search_type="similarity", search_kwargs={"k": 1})

# ✅ 7. ChatOpenAI도 키를 명시적으로 전달
chat = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key
)
