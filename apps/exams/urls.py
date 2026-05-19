from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('<int:exam_id>/', views.start_exam, name='start_exam'),
    path('<int:exam_id>/submit/', views.submit_exam, name='submit_exam'),
]
