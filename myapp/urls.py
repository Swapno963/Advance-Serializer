from django.urls import path
from . import views

urlpatterns = [
    path('products_basic/', views.product_list_basic),
    path('products_detail/', views.product_list_detail),
    path('products/<int:pk>/', views.product_detail),
    path('orders/', views.order_list),

]