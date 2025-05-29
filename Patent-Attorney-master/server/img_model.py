import os
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 사전 학습된 모델 로드 (ResNet18)
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()

# 전처리 함수
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# 이미지 1장의 특징 추출
def extract_feature(img_path):
    image = Image.open(img_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        features = model(image)
    return features.squeeze().numpy()

# 전체 이미지 인덱스 초기화
def initialize_index(folder):
    paths, features = [], []
    for fname in os.listdir(folder):
        if fname.lower().endswith(('.jpg', '.png', '.jpeg')):
            full = os.path.join(folder, fname)
            feat = extract_feature(full)
            paths.append(full)
            features.append(feat)
    return paths, np.array(features)

# 유사 이미지 검색
def search_similar(img_path, db_paths, db_features, top_k=5):
    uploaded_feat = extract_feature(img_path).reshape(1, -1)
    similarities = cosine_similarity(uploaded_feat, db_features)[0]
    ranked = sorted(zip(db_paths, similarities), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
