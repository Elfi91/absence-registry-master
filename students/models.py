from django.db import models

def generate_matricola():
    """
    Genera una matricola unica progressiva con formato STU00001.
    Controlla l'ultimo studente salvato e incrementa il numero.
    """
    last_student = Student.objects.order_by('-id').first()

    if last_student and last_student.matricola:
        try:
            last_number = int(last_student.matricola[3:])
        except ValueError:
            last_number = 0
    else:
        last_number = 0

    new_number = last_number + 1
    return f"STU{new_number:05d}"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course = models.CharField(
        max_length=10,
        help_text="es: DEV, DSGN, PHOTOGRAPH, WEB, etc."
    )
    matricola = models.CharField(
        max_length=20,
        unique=True, 
        blank=True
        )

    class Meta:
        verbose_name_plural = "Students"
        # AGGIUNTA IMPORTANTE:
        # Questo vincolo impedisce a livello di Database di avere duplicati
        # Coincide con la logica che abbiamo scritto nel Serializer.
        unique_together = ['first_name', 'last_name', 'course']

    def save(self, *args, **kwargs):
        """
        Se la matricola non esiste, la genera automaticamente.
        """
        if not self.matricola:
            self.matricola = generate_matricola()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.course}) - {self.matricola}"