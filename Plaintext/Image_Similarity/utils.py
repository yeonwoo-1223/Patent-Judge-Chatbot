# image_similarity/urls.py

from django.urls import path
from Painttext.Patent_Attorney.api.views import ImageSimilarityAPIView

urlpatterns = [
    path('similarity/', ImageSimilarityAPIView.as_view(), name='image-similarity'),
]
