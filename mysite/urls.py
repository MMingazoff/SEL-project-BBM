"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import exam_testing.views as views

urlpatterns = [
    path('', views.headpage),
    path('non_auth/', views.headpage_non_auth),
    path('admin/', admin.site.urls),
    path('exam/', include('exam_testing.urls')),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('register/', views.register),
    path('recover/', views.recover_password),
]
