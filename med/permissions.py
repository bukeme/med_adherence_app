from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAccountOrAdminReadOnly(BasePermission):
	def has_obj_permission(self, request, view, obj):
		if request.user == obj or request.user.admin:
			if request.method in SAFE_METHODS:
				return True
			else:
				return request.user == obj
		return False

class IsMedAccountOrAdminReadOnly(BasePermission):
	def has_obj_permission(self, request, view, obj):
		if obj.patient == request.user or request.user.admin:
			if request.method in SAFE_METHODS:
				return True
			else:
				return obj.patient == request.user
		return False

class IsMedDoseAccountOrAdminReadOnly(BasePermission):
	def has_obj_permission(self, request, view, obj):
		if obj.medication.patient == request.user or request.user.admin:
			if request.method in SAFE_METHODS:
				return True
			else:
				return obj.medication.patient == request.user
		return False