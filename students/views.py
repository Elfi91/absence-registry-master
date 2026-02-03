from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer


class StudentListView(generics.ListCreateAPIView):
    """
    GET: Lista tutti gli studenti
    POST: Crea un nuovo studente (solo Admin)
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Dettagli di uno studente
    PUT/PATCH: Aggiorna lo studente (anche parzialmente)
    DELETE: Elimina lo studente
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        """
        Gestisce aggiornamenti parziali (PATCH) con validazione migliorata
        Permette agli studenti di modificare i propri dati
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Valida i dati
        if serializer.is_valid():
            self.perform_update(serializer)

            return Response({
                'message': 'Profilo aggiornato con successo',
                'student': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Dati non validi',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Gestisce aggiornamenti completi (PUT)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'message': 'Aggiornamento completato con successo',
                'student': serializer.data
            })
        else:
            return Response({
                'error': 'Dati non validi',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)