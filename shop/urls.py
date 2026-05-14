from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),
]
