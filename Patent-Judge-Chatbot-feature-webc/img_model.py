import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# ResNet50 기반 특징 추출기
class FeatureExtractor(nn.Module):
    def __init__(self):
        super(FeatureExtractor, self).__init__()
        model = models.resnet50(pretrained=True)
        self.features = nn.Sequential(*list(model.children())[:-1])  # 마지막 분류기 제거

    def forward(self, x):
        with torch.no_grad():
            x = self.features(x)
            return x.view(x.size(0), -1)

# 이미지 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# 학습 데이터 특징 추출
def load_dataset_features(base_dir):
    extractor = FeatureExtractor().eval()
    image_paths, features = [], []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(root, file)
                try:
                    image = Image.open(path).convert('RGB')
                    tensor = transform(image).unsqueeze(0)
                    feature = extractor(tensor).squeeze().numpy()
                    image_paths.append(path)
                    features.append(feature)
                except Exception as e:
                    print(f"Error loading {path}: {e}")
    return image_paths, np.array(features)

# 입력 이미지와 유사도 비교
def find_similar_images(input_path, dataset_paths, dataset_features, top_k=5):
    extractor = FeatureExtractor().eval()
    image = Image.open(input_path).convert('RGB')
    tensor = transform(image).unsqueeze(0)
    input_feature = extractor(tensor).squeeze().numpy().reshape(1, -1)
    
    sims = cosine_similarity(input_feature, dataset_features)[0]
    top_indices = np.argsort(sims)[::-1][:top_k]
    return [(dataset_paths[i], sims[i]) for i in top_indices]

# 유사 이미지 시각화
def display_similar_images(results):
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False
  
    fig, axes = plt.subplots(1, len(results), figsize=(15, 5))
    for i, (path, score) in enumerate(results):
        img = Image.open(path)
        file_name, file_extension = os.path.splitext(os.path.basename(path))

        axes[i].imshow(img)
        axes[i].set_title(f"출원번호: {file_name}\n유사도: {score*100:.2f}%")
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

def initialize_index(train_folder):
    """
    학습용 이미지 폴더에서 특징 벡터를 한 번만 로드합니다.
    Returns:
        paths: 이미지 파일 경로 리스트
        features: 각 이미지의 특징 벡터 리스트
    """
    paths, features = load_dataset_features(train_folder)
    return paths, features

def search_similar(input_image_path, paths, features, top_k=5):
    """
    업로드된 이미지를 받아서 top_k개 유사 이미지 경로와 유사도 리스트를 반환합니다.
    """
    similar = find_similar_images(input_image_path, paths, features)[:top_k]
    return similar


# # 사용 예시
# if __name__ == "__main__":
#     train_folder = "./Resources/mark_img"  # 상표 이미지들이 있는 폴더

#     file_name, file_extension = os.path.splitext(os.path.basename(path))
#     input_image_path = f"./uploads/{file_name}{file_extension}"  # 사용자가 업로드한 이미지

#     print("이미지 특징 추출 중...")
#     paths, features = load_dataset_features(train_folder)
    
#     print("유사 이미지 검색 중...")
#     similar = find_similar_images(input_image_path, paths, features)
    
#     print("결과 출력:")
#     display_similar_images(similar)