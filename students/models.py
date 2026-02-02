from django.db import models
from datetime import date

class Student(models.Model):
    """Rappresenta l'anagrafica di uno studente."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course = models.CharField(max_length=10)

    class Meta:
        # Corregge il nome plurale nell'interfaccia di amministrazione (evita "Studentss")
        verbose_name_plural = "Students"

    @property
    def presence_percentage(self):
        """
        CAMPO CALCOLATO (Logic Property):
        Questo dato non esiste fisicamente nel database. Viene calcolato
        ogni volta che lo richiediamo, basandosi sulla data di oggi.
        """

        # 1. Impostiamo una data fissa di inizio corso
        start_date = date(2025, 11, 23)
        today = date.today()

        # 2. Calcolo giorni totali di corso trascorsi (escludendo weekend)
        total_days_passed = (today - start_date).days + 1

        if total_days_passed <= 0:
            return 100.0

        # 3. Contiamo le assenze nel DB.
        # 'self.absences' funziona grazie al related_name='absences' definito nel modello Absence.
        # Filtriamo solo le assenze fino a oggi (date__lte=today).
        absence_count = self.absences.filter(date__lte=today).count()

        # 4. Formula matematica della percentuale di presenza
        percentage = ((total_days_passed - absence_count) / total_days_passed) * 100

        # Restituiamo il valore arrotondato a 2 decimali, assicurandoci che non sia mai negativo
        return round(max(0, percentage), 2)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.course})"