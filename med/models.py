from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Medication(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE)
	drug_name = models.CharField(max_length=250)
	drug_form = models.CharField(max_length=250)
	medication_reason = models.TextField()
	num_of_dose = models.IntegerField()


class MedicationDose(models.Model):
	medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
	set_time = models.DateTimeField()
	taken_at = models.DateTimeField(null=True, blank=True)
	taken = models.BooleanField(default=False)
