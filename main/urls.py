from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [ 
    path('products_list', views.products_list, name='products_list'),
    path('products_upload', views.products_upload, name='products_upload'),
]