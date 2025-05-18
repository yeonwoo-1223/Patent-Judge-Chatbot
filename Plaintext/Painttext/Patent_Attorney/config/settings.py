import os
import json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'config/secrets.json'), encoding='utf-8') as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {setting} environment variable")

# OPENAPI_KEY = get_secret("OPENAPI_KEY")  # 필요 시 설정


# 2. api/views.py (유사 이미지 결과 반환 뷰 추가)
from rest_framework.views import APIView
from rest_framework.response import Response
from Painttext.Patent_Attorney.api.models import MarkPatentInfo, DesignPatentInfo
from serializers import SimilarityResultSerializer
from Image_Similarity.similarity import find_similar_images

class SimilarImageView(APIView):
    def post(self, request):
        uploaded_image = request.FILES.get('image')
        if not uploaded_image:
            return Response({"error": "이미지를 업로드해주세요."}, status=400)

        results = find_similar_images(uploaded_image)
        serializer = SimilarityResultSerializer(results, many=True)
        return Response(serializer.data)