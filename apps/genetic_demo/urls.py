from django.urls import path
from . import views

app_name = 'genetic_demo'

urlpatterns = [
    path('', views.genetic_demo_index, name='index'),
    path('result/', views.genetic_demo_result, name='result'),
]
