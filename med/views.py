from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
	RegisterMedicationSerializer,
	MedicationReportSerializer,
	PatientMedicationReportSerializer
)
from .models import Medication, MedicationDose

User = get_user_model()



class RegisterMedicationAPIView(generics.GenericAPIView):
	serializer_class = RegisterMedicationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		patient = request.user
		drug_name = serializer.validated_data.get('drug_name')
		drug_form = serializer.validated_data.get('drug_form')
		medication_reason = serializer.validated_data.get('medication_reason')
		num_of_dose = serializer.validated_data.get('num_of_dose')
		set_times = serializer.validated_data.get('set_times')

		if num_of_dose != len(set_times):
			return Response({
				'error': 'Number of set times is not equal to number of doses',
				'status': status.HTTP_400_BAD_REQUEST
			}, status=status.HTTP_400_BAD_REQUEST)

		medication = Medication.objects.create(
			patient=patient,
			drug_name=drug_name,
			drug_form=drug_form,
			medication_reason=medication_reason,
			num_of_dose=num_of_dose
		)

		for set_time in set_times:
			MedicationDose.objects.create(
				medication=medication,
				set_time=set_time
			)
		return Response({
			'medication': MedicationReportSerializer(medication).data,
			'status': status.HTTP_200_OK
		}, status=status.HTTP_200_OK)

register_medication = RegisterMedicationAPIView.as_view()

class PatientMedicationReportAPIView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = PatientMedicationReportSerializer
	permission_classes = [permissions.IsAuthenticated]

patient_medication_report = PatientMedicationReportAPIView.as_view()

class MedicationRetrieveUpdateDestroyAPIView(viewsets.ModelViewSet):
	queryset = Medication.objects.all()
	serializer_class = MedicationReportSerializer
	permission_classes = [permissions.IsAuthenticated]

medication_retrieve = MedicationRetrieveUpdateDestroyAPIView.as_view({'get': 'retrieve'})
medication_update = MedicationRetrieveUpdateDestroyAPIView.as_view({'put': 'update'})
medication_destroy = MedicationRetrieveUpdateDestroyAPIView.as_view({'delete': 'destroy'})
