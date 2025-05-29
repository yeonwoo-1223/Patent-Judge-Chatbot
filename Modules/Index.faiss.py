import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. .env 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
api_key = os.getenv("OPENAI_API_KEY")
print("✅ API KEY:", api_key[:10] + "...")

# 2. 임베딩 모델
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=api_key
)

# 3. 특허 관련 텍스트 예시
texts = [
    "특허법 제29조는 신규성과 진보성에 대한 기준을 규정한다.",
    "공개된 기술은 특허를 받을 수 없다.",
    "직무발명의 권리는 원칙적으로 사용자에게 귀속된다.",
    "무효심판은 등록된 특허의 유효성에 대해 이의를 제기하는 절차이다.",
    "특허 침해가 인정되면 손해배상 및 금지청구가 가능하다."
]

# 4. 저장 경로 설정
vector_dir = Path(__file__).resolve().parent.parent / "Resources/vector_store_law"
vector_dir.mkdir(parents=True, exist_ok=True)

# 5. 벡터 인덱스 생성 및 저장
print("⚙️ 벡터 인덱스 생성 중...")
vector_store = FAISS.from_texts(texts, embeddings)
vector_store.save_local(str(vector_dir))
print("✅ 저장 완료:", vector_dir / 'index.faiss')
