from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


# patent-attorney/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from Image_Similarity.similarity import find_similar_images  # 벡터 비교 함수
from PIL import Image

class ImageSimilarityAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            image = Image.open(image_file)

            # 유사 이미지 찾기 (유사도 순 정렬된 리스트 반환)
            results = find_similar_images(image)

            return Response({'results': results}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# patent-attorney/api/urls.py
from django.urls import path
from .views import ImageSimilarityAPIView

urlpatterns = [
    path('similarity/', ImageSimilarityAPIView.as_view(), name='image-similarity'),
]