from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from med.models import Medication, MedicationDose

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		temp_med = [
			{
				'drug_name': 'Paracetamol',
				'drug_form': 'Tablet',
				'medication_reason': 'Headache'
			},
			{
				'drug_name': 'Aspirin',
				'drug_form': 'Capsule',
				'medication_reason': 'Body Pain'
			},
			{
				'drug_name': 'Septrin',
				'drug_form': 'Tablet',
				'medication_reason': 'Chest Pain'
			}
		]
		for _ in range(5):
			full_name = fake.name()
			user = User.objects.create_user(
				full_name=full_name,
				email=''.join(full_name.split()) + '@company.com',
				password='testing321',
				phone='134917340901'
			)
			self.stdout.write(self.style.SUCCESS('Created Patient'))

			for temp in temp_med:
				med = Medication.objects.create(
					patient=user,
					drug_name=temp['drug_name'],
					drug_form=temp['drug_form'],
					medication_reason=temp['medication_reason'],
					num_of_dose=3
				)
				self.stdout.write(self.style.SUCCESS('Created Medication'))
				for i in range(27, 31):
					MedicationDose.objects.create(
						medication=med,
						set_time=f'2023-11-{i}T08:00:01.630000Z'
					)
					self.stdout.write(self.style.SUCCESS('Created Medication Dose'))
		for _ in range(5):
			full_name = fake.name()
			user = User.objects.create_superuser(
				full_name=full_name,
				email=''.join(full_name.split()) + '@company.com',
				password='testing321',
				phone='134917340901'
			)
			self.stdout.write(self.style.SUCCESS('Created Doctor'))
		self.stdout.write(self.style.SUCCESS('Data seeded successfully'))
