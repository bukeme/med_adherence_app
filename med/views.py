from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils import timezone
from .serializers import (
	RegisterMedicationSerializer,
	MedicationReportSerializer,
	PatientMedicationReportSerializer,
	MedicationDoseSerializer
)
from .models import Medication, MedicationDose
from .permissions import IsAccountOrAdminReadOnly, IsMedAccountOrAdminReadOnly, IsMedDoseAccountOrAdminReadOnly

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
	permission_classes = [permissions.IsAuthenticated, IsAccountOrAdminReadOnly]

patient_medication_report = PatientMedicationReportAPIView.as_view()

class MedicationRetrieveUpdateDestroyAPIView(viewsets.ModelViewSet):
	queryset = Medication.objects.all()
	serializer_class = MedicationReportSerializer
	permission_classes = [permissions.IsAuthenticated, IsMedAccountOrAdminReadOnly]

medication_retrieve = MedicationRetrieveUpdateDestroyAPIView.as_view({'get': 'retrieve'})
medication_update = MedicationRetrieveUpdateDestroyAPIView.as_view({'patch': 'partial_update'})
medication_destroy = MedicationRetrieveUpdateDestroyAPIView.as_view({'delete': 'destroy'})

class MedicationDoseViewSet(viewsets.ModelViewSet):
	queryset = MedicationDose.objects.all()
	serializer_class = MedicationDoseSerializer
	permission_classes = [permissions.IsAuthenticated]

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		taken_initial = instance.taken
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		drug_taken = request.data.get('taken', None)
		dose = serializer.save()
		if drug_taken != None:
			if taken_initial == True and drug_taken == 'false':
				dose.taken_at = None
				dose.save()
			elif taken_initial == False and drug_taken == 'true':
				dose.taken_at = timezone.now()
				dose.save()
		
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		med_dose = serializer.save()
		doses_count = med_dose.medication.num_of_dose
		med_dose.medication.num_of_dose = doses_count + 1
		med_dose.medication.save()
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		medication = instance.medication
		self.perform_destroy(instance)
		doses_count = medication.num_of_dose
		medication.num_of_dose = doses_count - 1
		medication.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

medication_dose_create = MedicationDoseViewSet.as_view({'post': 'create'})
medication_dose_update = MedicationDoseViewSet.as_view({'patch': 'partial_update'})
medication_dose_delete = MedicationDoseViewSet.as_view({'delete': 'destroy'})
