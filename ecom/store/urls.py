
from django.urls import path
from . import views

urlpatterns = [
    # Main
    path('', views.store, name='store'),
    
    # Individual Product
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    
    # Individual Category
    path('search/<slug:category_slug>/', views.list_category, name='list_category'),
]
