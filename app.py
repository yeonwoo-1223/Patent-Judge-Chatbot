from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI  # openai 임포트는 하지 말라는 점 기억

# 🔐 API 키 불러오기
with open("api_key.txt", "r") as f:
    api_key = f.read().strip()

# OpenAI 클라이언트 생성 (키 직접 넘기기)
client = OpenAI(api_key=api_key)

app = Flask(__name__)

# 홈화면
@app.route('/')
def index():
    return render_template('index.html')

# 이미지 업로드 처리
@app.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if image:
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        image.save(os.path.join('uploads', image.filename))
        return render_template('index.html', result=f"'{image.filename}' 업로드 완료!")
    return render_template('index.html', result="이미지 업로드 실패")

# 질문 처리 및 GPT 호출 (비동기 JSON 반환)
@app.route('/ask_bot', methods=['POST'])
def ask_bot():
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': '질문을 입력해주세요.'})

    try:
        # GPT 호출 부분 (임시 더미 응답)
        # 실제로는 client.chat.completions.create 호출해서 사용
        answer = f"GPT 응답 자리 (질문: {question})\n\n[여기에 GPT 응답이 표시될 예정입니다.]"

    except Exception as e:
        return jsonify({'error': f"GPT 호출 중 오류 발생: {str(e)}"})

    return jsonify({'answer': answer})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
