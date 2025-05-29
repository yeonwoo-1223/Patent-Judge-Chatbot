import os
import torch
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 사전 학습된 모델 (ResNet18)
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()

# 이미지 전처리 설정
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# 특징 벡터 추출 함수
def extract_features(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        features = model(image)
    return features.squeeze().numpy()

# 유사한 이미지 찾기
def find_similar_design(uploaded_image_path):
    base_path = "static/find_similar_images"
    uploaded_features = extract_features(uploaded_image_path)

    best_score = -1
    best_match = None

    for fname in os.listdir(base_path):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            candidate_path = os.path.join(base_path, fname)
            candidate_features = extract_features(candidate_path)

            score = cosine_similarity(
                uploaded_features.reshape(1, -1),
                candidate_features.reshape(1, -1)
            )[0][0]

            if score > best_score:
                best_score = score
                best_match = fname

    return {"best_match": best_match, "score": round(float(best_score), 4)}
