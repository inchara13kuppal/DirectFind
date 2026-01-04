from django.contrib import admin
from django.urls import path
from recommender import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),
]
