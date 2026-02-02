from django.db import models
from django.contrib.auth.models import User
from students.models import Student

class Absence(models.Model):
    """Rappresenta una singola assenza di uno studente in una data specifica."""

    # Collegamento allo studente: related_name='absences' ci permette di scrivere
    # student.absences.all() per ottenere tutte le assenze di quello studente.
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='absences')

    date = models.DateField()
    is_justified = models.BooleanField(default=False)

    # Audit Trail: Salviamo chi ha creato l'assenza (es. il Professore).
    # on_delete=models.SET_NULL: Se il prof viene cancellato, non cancelliamo le assenze,
    # ma il campo 'created_by' diventa vuoto (NULL) per preservare lo storico.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.student} - {self.date}"