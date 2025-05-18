# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('image_similarity.urls')),  # 이 줄이 추가되어야 API가 활성화됩니다
]