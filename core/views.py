from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from students.models import Student
from students.serializers import StudentSerializer

from .models import Absence
from .serializers import AbsenceSerializer, RegisterSerializer, ChangePasswordSerializer


class ChangePasswordView(APIView):
    """Endpoint per cambiare la password. Richiede autenticazione."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            # set_password si occupa dell'hashing della nuova password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password aggiornata correttamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbsenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """"
    Gestisce le operazioni su una SINGOLA assenza:
    - GET: Leggi dettagli
    - PUT/PATCH: Modifica (es. giustifica assenza)
    - DELETE: Rimuovi assenza
    """
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    """
    Endpoint di registrazione.
    Usa AllowAny perché un utente non loggato deve poter creare un account.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class AbsenceCreateView(generics.ListCreateAPIView):
    """Gestisce la lista delle assenze (GET) e la creazione di nuove (POST)."""
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # AUTOMATISMO:
        # Quando viene creata un'assenza, non chiediamo all'utente di inserire il proprio ID.
        # Intercettiamo il salvataggio e inseriamo automaticamente l'utente loggato (request.user)
        # nel campo 'created_by'.
        # Questo salva l'utente che sta usando Postman come "creatore" dell'assenza
        serializer.save(created_by=self.request.user)