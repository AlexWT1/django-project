from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name="index"),
    path('post_modal/', views.post_modal, name='post_modal'),
    path('post_modal_api/', views.post_modal_api, name='post_modal_api'),
    path('notification_modal/', views.notification_modal, name='notification_modal'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

