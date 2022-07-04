from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.test_results, name='test_results'),
]