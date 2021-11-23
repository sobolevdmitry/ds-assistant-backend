from django.urls import path
from . import views

urlpatterns = [
    path('write', views.write, name='write'),
    path('read', views.write, name='read'),
    path('get-data', views.get_data, name='get-data')
]
