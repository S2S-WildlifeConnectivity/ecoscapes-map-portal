from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, {'page_name': 'default'}, name='map_view'),
    path('api/panorama-config/', views.panorama_config, name='panorama_config'),
    path('<str:page_name>/', views.map_view, name='map_view_with_page'),
]
