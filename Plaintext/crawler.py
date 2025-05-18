# crawler.py (Plaintext 폴더에 있어야 함)
import os
import sys
import django
import unicodedata

# [1] sys.path에 경로 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'Painttext'))

# [2] DJANGO_SETTINGS_MODULE 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Painttext.Patent_Attorney.config.settings')

# [3] Django 초기화
django.setup()

# [4] 모델 임포트
from Painttext.Patent_Attorney.api.models import MarkPatentInfo, DesignPatentInfo
from Painttext.Patent_Attorney.api.utils import create_model_instance

# [5] train 디렉토리 경로
TRAIN_DIR = os.path.join(BASE_DIR, 'train')

# [6] 크롤링 / DB 저장 예시
if __name__ == '__main__':
    mark_list = []  # 예시
    design_list = ['의자']  # 예시

    dirs = os.listdir(TRAIN_DIR)
    for dir_name in dirs:
        dir_path = os.path.join(TRAIN_DIR, dir_name)
        dir_name = unicodedata.normalize('NFC', dir_name)
        if dir_name in mark_list:
            filenames = os.listdir(dir_path)
            filenames = [os.path.splitext(f)[0] for f in filenames]
            for filename in filenames:
                create_model_instance(filename, 0, dir_name)
        elif dir_name in design_list:
            filenames = os.listdir(dir_path)
            filenames = [os.path.splitext(f)[0] for f in filenames]
            filenames.sort()
            for count, filename in enumerate(filenames):
                if count == 100:
                    break
                create_model_instance(filename, 1, dir_name)
