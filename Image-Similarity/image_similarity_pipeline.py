import os
import cv2
import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity


# 2. 이미지 벡터화 함수
def image_to_vector(image_path):
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    img_np = np.array(img)
    img_flat = img_np.flatten().astype(np.float32)
    img_norm = img_flat / np.linalg.norm(img_flat)
    return img_norm

# 3. 유사도 비교 함수
def compare_images(image_path1, image_path2):
    vec1 = image_to_vector(image_path1)
    vec2 = image_to_vector(image_path2)
    similarity = cosine_similarity([vec1], [vec2])[0][0]
    return similarity * 100  # 퍼센트로 변환

# === 사용 예시 ===
if __name__ == "__main__":
    # Step 1: 이미지 크롤링
    search_term = "cat"
    crawled_images = crawl_images(search_term, num_images=3)
    if len(crawled_images) < 2:
        print("[-] Not enough images to compare.")
        exit()

    # Step 2 & 3: 이미지 유사도 비교
    for i in range(1, len(crawled_images)):
        sim = compare_images(crawled_images[0], crawled_images[i])
        print(f"[✓] Similarity between image 0 and image {i}: {sim:.2f}%")
