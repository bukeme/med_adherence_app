from django.urls import path
from . import views


urlpatterns = [
	path('register-medication/', views.register_medication, name='register_medication'),
	path('medication/<int:pk>/', views.medication_retrieve, name='medication_retrieve'),
	path('medication/<int:pk>/update/', views.medication_update, name='medication_update'),
	path('medication/<int:pk>/delete/', views.medication_destroy, name='medication_destroy'),
	path('patient-report/<int:pk>/', views.patient_medication_report, name='patient_report'),
]