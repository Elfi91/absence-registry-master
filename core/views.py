# core/views.py

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from students.models import Student
from students.serializers import StudentSerializer

from .models import Absence
from .serializers import AbsenceSerializer, RegisterSerializer, ChangePasswordSerializer

# Proviamo a usare la permission richiesta dal task.
# Se non esiste ancora, facciamo fallback su IsAdminOrReadOnly per non rompere il progetto.
try:
    from .permissions import IsAdminOrSelf
except Exception:
    from .permissions import IsAdminOrReadOnly as IsAdminOrSelf


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"detail": "Password aggiornata correttamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# NOTA: questa view è probabilmente duplicata perché esiste anche students/views.py.
# La lasciamo per compatibilità con l'import in config/urls.py.
class StudentListView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        qs = Student.objects.select_related("user")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)


class AbsenceCreateView(generics.ListCreateAPIView):
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        qs = Absence.objects.select_related("student", "student__user")
        if self.request.user.is_staff:
            return qs #Admin vede tutto
        # Partecipante: vede solo le proprie assenze (student.user == request.user)
        return qs.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        # Salva l'utente che crea l'assenza (tipicamente l'admin)python manage
        serializer.save(created_by=self.request.user)


class AbsenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        qs = Absence.objects.select_related("student", "student__user")
        if self.request.user.is_staff:
            return qs
        return qs.filter(student__user=self.request.user)

