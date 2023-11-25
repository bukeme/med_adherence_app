from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Medication, MedicationDose
from accounts.serializers import UserSerializer

User = get_user_model()


class RegisterMedicationSerializer(serializers.Serializer):
	drug_name = serializers.CharField()
	drug_form = serializers.CharField()
	medication_reason = serializers.CharField()
	num_of_dose = serializers.IntegerField()
	set_times = serializers.ListField(
		child=serializers.DateTimeField(),
		allow_empty=False
	)

class MedicationDoseSerializer(serializers.ModelSerializer):
	class Meta:
		model = MedicationDose
		fields = ['pk', 'set_time', 'taken_at', 'taken']

class MedicationReportSerializer(serializers.ModelSerializer):
	patient = UserSerializer(many=False, read_only=True)
	medication_doses = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Medication
		fields = ['pk', 'patient', 'drug_name', 'drug_form', 'medication_reason', 'num_of_dose', 'medication_doses',]

	def get_medication_doses(self, obj):
		qs = MedicationDose.objects.filter(medication=obj)
		return MedicationDoseSerializer(qs, many=True, context=self.context).data

class SubMedicationReportSerializer(MedicationReportSerializer):
	class Meta:
		model = Medication
		fields = ['pk', 'drug_name', 'drug_form', 'medication_reason', 'num_of_dose', 'medication_doses',]

class PatientMedicationReportSerializer(serializers.ModelSerializer):
	medications = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = User
		fields = ['pk', 'full_name', 'email', 'medications']

	def get_medications(self, obj):
		qs = Medication.objects.filter(patient=obj)
		return SubMedicationReportSerializer(qs, many=True, context=self.context).data
