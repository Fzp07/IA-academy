from django.urls import path
from . import views

app_name = 'regression_demo'

urlpatterns = [
    path('', views.regression_demo_index, name='index'),
    path('result/', views.regression_demo_result, name='result'),
]
