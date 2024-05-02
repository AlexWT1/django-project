from django.contrib import admin
from django.urls import path, include
from posts import views as posts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', posts_views.post_list, name='post_list'),  # Использование представления post_list для главной страницы
    path('post/<int:pk>/', posts_views.post_detail, name='post_detail'),  # Путь для детальной страницы поста
    path('users/', include('users.urls')),  # URL-адреса пользователей
    path('posts/', include('posts.urls')),  # URL-адреса постов
    path('api/', include('apiYandex.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
