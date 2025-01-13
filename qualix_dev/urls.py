from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Панель администратора
    path("", include("api.urls")),   # Подключаем маршруты приложения "api"
]
