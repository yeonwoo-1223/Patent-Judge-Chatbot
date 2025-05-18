import numpy as np
from PIL import Image

def preprocess(image: Image.Image):
    image = image.resize((224, 224)).convert('RGB')
    arr = np.array(image).astype('float32') / 255.0
    return arr.reshape(1, -1)  # 단순 벡터화 (예시)