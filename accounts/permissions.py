from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )


class IsPatientRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'PATIENT'
        )


class IsPrimaryStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_primary_staff and
            request.user.is_approved
        )


class IsSpecialistStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_specialist_staff and
            request.user.is_approved
        )


class IsAnyStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_any_staff and
            request.user.is_approved
        )


class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role == 'ADMIN':
            return True
        return request.user.is_any_staff and request.user.is_approved


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        if request.user.is_any_staff and request.user.is_approved:
            return True
        if hasattr(obj, 'patient'):
            return obj.patient == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False