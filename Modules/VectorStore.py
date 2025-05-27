import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

print("✅ VectorStore.py 실행됨")

# .env 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
api_key = os.getenv("OPENAI_API_KEY")
print("🔐 OPENAI_API_KEY 불러오기 성공:", api_key[:10] + "...")

# 임베딩
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=api_key
)

# 저장된 벡터 인덱스 경로 (절대 경로)
vector_dir = Path(__file__).resolve().parent.parent / "Resources/vector_store_law"

# 저장된 벡터 인덱스를 로드
vector_store_law = FAISS.load_local(
    str(vector_dir),
    embeddings,
    allow_dangerous_deserialization=True
)

# 리트리버, 챗 모델 생성
retriever = vector_store_law.as_retriever(search_kwargs={"k": 5})
chat = ChatOpenAI(model="gpt-4o", openai_api_key=api_key)
