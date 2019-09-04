from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('app.urls')),
    path('auth/admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='reg/login.html'), name='login'),
    path('accounts/logout/', auth_views.LoginView.as_view(template_name='reg/login.html'), name='logout'),
]