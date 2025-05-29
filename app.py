import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from img_model import find_similar_design
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Flask 앱 초기화
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 크롤링 기반 판례 검색기 초기화
def load_qa():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = FAISS.load_local("Resources/vector_store_law", embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    return RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

qa = load_qa()

# 라우팅
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = qa.run(user_message)
    return jsonify({'response': response})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '파일명이 없습니다.'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    result = find_similar_design(filepath)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
