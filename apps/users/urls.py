from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('reset-password/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('reset-password/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset-admin/', views.reset_admin, name='reset_admin'),
]
