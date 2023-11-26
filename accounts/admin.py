from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Register your models here.

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm

	list_display = ['email', 'full_name', 'phone', 'is_active', 'admin']
	list_filter = ['email', 'is_active', 'admin']
	fieldsets = (
		(None, {'fields': ('email',)}),
		('Personal', {'fields': ('full_name', 'phone',)}),
		('Permissions', {'fields': ('admin',)}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('full_name', 'phone', 'email', 'password', 'password_2')	
		}),
	)
	search_fields = ['email',]
	ordering = ['-date_joined']

admin.site.register(User, UserAdmin)
