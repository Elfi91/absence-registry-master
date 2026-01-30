# core/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSelf(BasePermission):
    """
    Admin (is_staff=True): accesso completo
    Partecipante: solo lettura, e solo sui propri oggetti
    """

    def has_permission(self, request, view):
        # se usi anche IsAuthenticated in permission_classes, questa è ridondante ma ok
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin -> tutto
        if request.user.is_staff:
            return True

        # Partecipante -> solo GET/HEAD/OPTIONS
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Admin -> tutto
        if request.user.is_staff:
            return True

        # Partecipante -> solo lettura
        if request.method not in SAFE_METHODS:
            return False

        # Caso 1: oggetto con field "user" (es. Student.user)
        if hasattr(obj, "user"):
            return obj.user == request.user

        # Caso 2: oggetto che punta a student -> user (es. Absence.student.user)
        if hasattr(obj, "student") and hasattr(obj.student, "user"):
            return obj.student.user == request.user

        return False

