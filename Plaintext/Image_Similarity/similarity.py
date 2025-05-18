from .preprocessing import preprocess_image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# 특징 벡터 불러오기
feature_vectors = np.load('Image-Similarity/features.npy')
with open('Image-Similarity/image_paths.pkl', 'rb') as f:
    image_paths = pickle.load(f)

def find_similar_images(pil_image, top_k=5):
    query_vec = preprocess_image(pil_image).reshape(1, -1)
    similarities = cosine_similarity(query_vec, feature_vectors)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            'image_path': image_paths[idx],
            'similarity': round(float(similarities[idx] * 100), 2)
        })
    return results


# 최상위 URL 설정: patent-attorney/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # 이 줄 추가
]