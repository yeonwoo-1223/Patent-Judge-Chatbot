from flask import Flask, render_template, request, jsonify, url_for
import os
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from img_model import initialize_index, search_similar

load_dotenv()

# 🔐 API 키 불러오기 .env에서 키 불러옴
api_key = os.getenv("OPENAI_API_KEY")
print(f"DEBUG: Loaded API Key? {'Yes' if api_key else 'No'}")
if not api_key:
    raise ValueError("OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다.")

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key) 

app = Flask(__name__)

# ——— 이미지 유사도 모델 미리 로드 ———
TRAIN_FOLDER = "./static/find_similar_images"
IMG_PATHS, IMG_FEATURES = initialize_index(TRAIN_FOLDER)

# 홈화면
@app.route('/')
def index():
    return render_template('index.html')

# 이미지 업로드 처리
@app.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if not image:
        return jsonify({'error': '이미지 업로드 실패'}), 400

    # 1) 업로드된 파일 저장
    upload_dir = './static/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    filename = image.filename
    input_path = os.path.join(upload_dir, filename)
    image.save(input_path)

    # 2) 이미지 유사도 검색
    try:
        similar = search_similar(input_path, IMG_PATHS, IMG_FEATURES, top_k=5)
    except Exception as e:
        import traceback
        traceback.print_exc()   # 터미널에 전체 스택 트레이스 출력
        # 클라이언트에도 오류 메시지 내려줍니다.
        return jsonify({'error': f"이미지 유사도 검색 중 오류: {e}"}), 500

    # 3) 결과를 URL, 출원번호, 유사도 형태로 구조화
    results = []
    for path, score in similar:
        name = os.path.basename(path)
        app_no = os.path.splitext(name)[0]
        url = url_for('static', filename=f"find_similar_images/{name}", _external=False)
        results.append({
            'url': url,
            'application_number': app_no,
            'score': float(f"{score:.4f}")
        })

    # 4) 챗봇 말투용 요약 메시지(raw)
    lines = [f"✅ '{filename}' 업로드 완료! 유사한 이미지를 찾아볼게요."]
    for idx, r in enumerate(results, start=1):
        lines.append(f"{idx}. 출원번호 {r['application_number']} | 유사도 {r['score']*100:.2f}%")
    raw_message = "\n".join(lines)

    # 5) OpenAI Chat API 호출 → 자연스러운 대화체로 가공
    chat_messages = [
        {"role": "system", "content": "당신은 친절한 챗봇입니다. 아래 정보를 마크다운 이미지 태그(![출원번호](URL))를 사용해 이미지가 바로 보이도록 설명해주세요. 각 항목에 출원번호와 유사도도 함께 포함하세요."},
        {"role": "user",   "content": raw_message}
    ]
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_messages
        )
        bot_message = resp.choices[0].message.content
    except Exception as e:
        # RateLimitError 또는 기타 모든 오류 시에도 raw_message 로 graceful fallback
        print("▶ Chat API 오류:", e)
        bot_message = raw_message

    # 6) JSON 반환 (말풍선 텍스트 + 구조화된 결과)
    return jsonify({
        'answer': bot_message,
        'results': results
    })

# 질문 처리 및 GPT 호출 (비동기 JSON 반환)
@app.route('/ask_bot', methods=['POST'])
def ask_bot():
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': '질문을 입력해주세요.'})

    try:
        #FAISS 로드
        faiss_path = "Resources/vector_store_law" # 경로 확인
        vector_store = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

        #유사 문서 검색
        docs = vector_store.similarity_search(question, k=3)  # 상위 3개 문서

        #context 구성
        context = "\n\n".join([doc.page_content for doc in docs])

        #GPT 메시지 구성
        messages = [
            {
                "role": "system",
                "content": "당신은 법률 사건 문서를 기반으로 질문에 정확하고 간결하게 답하는 AI 비서입니다. 문서 내용을 바탕으로만 대답하세요."
                },
                {
                    "role": "user",
                    "content": f"다음은 참고할 문서입니다:\n\n{context}"
                    },
                    {
                         "role": "user",
                         "content": f"이 문서 기반으로 다음 질문에 답해주세요:\n\n{question}"
                         }
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message.content

    except Exception as e:
        return jsonify({'error': f"처리 중 오류 발생: {str(e)}"})

    return jsonify({'answer': answer})

if __name__ == '__main__':
    if not os.path.exists('./static/uploads'):
        os.makedirs('./static/uploads')
    app.run(debug=True)
