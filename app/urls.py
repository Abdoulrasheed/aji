from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('data/', views.get_data, name='get_data'),
]
