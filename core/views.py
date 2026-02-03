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
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password aggiornata correttamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbsenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class AbsenceCreateView(generics.ListCreateAPIView):
    """
    GET: Lista tutte le assenze
    POST: Crea una nuova assenza (solo Admin)
    """
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Salva l'assenza collegando correttamente lo studente
        e registrando chi ha creato l'assenza
        """
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Override per dare messaggi di errore più chiari
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            return Response({
                'message': 'Assenza registrata con successo',
                'absence': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'error': 'Dati non validi',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        """
        Opzionale: permette di filtrare le assenze per studente
        Esempio: /api/absences/?student=1
        """
        queryset = Absence.objects.all()
        student_id = self.request.query_params.get('student', None)
        
        if student_id is not None:
            queryset = queryset.filter(student__id=student_id)
        
        return queryset