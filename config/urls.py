from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import RegisterView, StudentListView, AbsenceCreateView, AbsenceDetailView, ChangePasswordView
from students.views import StudentDetailView, StudentListView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication Endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/password-change/', ChangePasswordView.as_view(), name='password_change'),

    # Students Endpoints
    path('api/students/', StudentListView.as_view(), name='student_list'),
    path('api/students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('api/absences/<int:pk>/', AbsenceDetailView.as_view(), name='absence-detail'),

    # Absences
    path('api/absences/', AbsenceCreateView.as_view(), name='absence_create'),
]