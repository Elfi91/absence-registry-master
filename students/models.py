from django.db import models
from datetime import date

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    classroom = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Students"

    @property
    def presence_percentage(self):
        # 1. Data di inizio corso (modificala in base alle vostre esigenze)
        start_date = date(2025, 11, 23)
        today = date.today()

        # 2. Calcolo giorni totali di corso trascorsi (escludendo weekend se vuoi essere precisa)
        total_days_passed = (today - start_date).days + 1

        if total_days_passed <= 0:
            return 100.0

        # 3. Conta le assenze dello studente (assumendo che la tabella Absences abbia un FK a Student)
        # Sostituisci 'absences' con il related_name corretto se diverso
        absence_count = self.absences.filter(date__lte=today).count()

        # 4. Formula finale
        percentage = ((total_days_passed - absence_count) / total_days_passed) * 100
        return round(max(0, percentage), 2)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.classroom})"