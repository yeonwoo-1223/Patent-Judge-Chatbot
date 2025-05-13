# FAISS 벡터 스토어 로드
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# 동일한 임베딩 모델 초기화 (FAISS 로드 시 필요)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# 로컬에서 로드
vector_store_law = FAISS.load_local(
    'Resources/vector_store_law', embeddings, allow_dangerous_deserialization=True)
vector_store_situation = FAISS.load_local(
    'Resources/vector_store_situation', embeddings, allow_dangerous_deserialization=True)
vector_store_rate = FAISS.load_local(
    'Resources/vector_store_rate', embeddings, allow_dangerous_deserialization=True)

# 유사성 검색 리트리버 정의
retriever = vector_store_law.as_retriever(
    search_type="similarity", search_kwargs={"k": 5})

retriever1 = vector_store_situation.as_retriever(
    search_type="similarity", search_kwargs={"k": 1})

retriever2 = vector_store_rate.as_retriever(
    search_type="similarity", search_kwargs={"k": 1})