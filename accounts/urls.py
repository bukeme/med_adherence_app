from django.urls import path
from . import views



urlpatterns = [
	path('create/', views.user_create, name='user_create'),
	path('list/', views.user_list_viewset, name='user_list'),
	path('<int:pk>/', views.user_detail_viewset, name='user_detail_viewset'),
	path('', views.user_detail, name='user_detail'),
	path('<int:pk>/update/', views.user_update_viewset, name='user_update'),
	path('change-password/', views.change_password, name='change_password'),
	path('password-reset/', views.password_reset, name='password_reset'),
	path('validate-password-reset-otp/', views.validate_password_reset_otp, name='validate_password_reset_otp'),
	path('confirm-password-reset/', views.confirm_password_reset, name='confirm_password_reset'),
	path('doctor-register/', views.doctor_register, name='doctor_register'),
]