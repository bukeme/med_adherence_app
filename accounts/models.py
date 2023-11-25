from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, full_name, email, password=None):
		if not email:
			raise ValueError('User must have an email address')

		email = self.normalize_email(email)

		user = self.model(
			full_name=full_name,
			email=email,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, full_name, email, password):
		user = self.create_user(
			full_name=full_name,
			email=email,
			password=password
		)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, full_name, email, password):
		user = self.create_user(
			full_name=full_name,
			email=email,
			password=password
		)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True
	)
	full_name = models.CharField(max_length=250)
	otp = models.CharField(max_length=50, null=True)
	is_active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name',]

	def __str__(self):
		return self.full_name

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_superuser(self):
		return self.admin
	
	
