from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('calculate-price/', views.CalculatePriceView.as_view(), name='calculate-price'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
]