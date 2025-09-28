from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('add/', views.add_ad, name='add_ad'),
    path('<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    path('<int:pk>/delete/', views.delete_ad, name='delete_ad'),
]
