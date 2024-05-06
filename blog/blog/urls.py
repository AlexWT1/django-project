from django.contrib import admin
from django.urls import path, include
from posts import views as posts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', posts_views.post_list, name='post_list'),
    path('main/', include('main.urls')),
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('api/', include('apiYandex.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
