from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main-page'),
    path('test/', views.test, name='testing'),
    path('results/', views.test_results, name='test-results'),
]
