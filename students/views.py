from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer

class StudentListView(generics.ListCreateAPIView):
    """
    Endpoint per la lista studenti.
    Gestisce automaticamente:
    1. GET: Restituisce la lista di tutti gli studenti.
    2. POST: Permette di creare un nuovo studente.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # Sicurezza: Solo gli utenti loggati (Admin/Teacher) possono vedere o creare studenti.
    permission_classes = [IsAuthenticated]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint per il singolo studente (cerca per ID).
    Gestisce automaticamente:
    1. GET: Dettagli studente specifico (+ lista assenze grazie al serializer).
    2. PUT/PATCH: Modifica dati studente.
    3. DELETE: Cancella studente.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]