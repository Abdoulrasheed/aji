from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('stat/', views.statistics, name='stats_page'),
    path('api/', views.load_graph_data, name='api_load_graph_data'),
    path('report/pdf/', views.generate_report, name='generate_report'),
]
