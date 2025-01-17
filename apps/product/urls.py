from django.urls import path

from .views import ProductDetail, ProductList, ProductCreate, ProductImageAddView

urlpatterns = [
    path('product-list/', ProductList.as_view(), name='product-list'),
    path('product-detail/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('product-create/', ProductCreate.as_view(), name='product-reviews'),
    path('product-create/<int:pk>/image/', ProductImageAddView.as_view(), name='product-image-add'),
]