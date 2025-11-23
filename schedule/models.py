from django.db import models

class Worker(models.Model):
    name = models.CharField("nombre", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ['name']

    def __str__(self):
        return self.name


class Day(models.Model):
    day_of_week = models.CharField(
        "día de la semana",
        max_length=10,
        choices=[
            ('Lun', 'Lunes'),
            ('Mar', 'Martes'),
            ('Mié', 'Miércoles'),
            ('Jue', 'Jueves'),
            ('Vie', 'Viernes'),
            ('Sáb', 'Sábado'),
            ('Dom', 'Domingo'),
        ],
        unique=True
    )

    class Meta:
        verbose_name = "Día"
        verbose_name_plural = "Días"
        ordering = ['id']

    def __str__(self):
        return self.get_day_of_week_display()


class Seat(models.Model):
    day = models.ForeignKey(
        Day,
        verbose_name="día",
        on_delete=models.CASCADE,
        related_name='seats'
    )
    worker = models.ForeignKey(
        Worker,
        verbose_name="trabajador",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='seats'
    )
    position = models.PositiveSmallIntegerField("posición", default=1)

    class Meta:
        verbose_name = "Asiento"
        verbose_name_plural = "Asientos"
        unique_together = ['day', 'position']
        ordering = ['day', 'position']

    def __str__(self):
        return f"{self.day.get_day_of_week_display()} - Posición {self.position}: {self.worker or 'Vacante'}"


class Skill(models.Model):
    name = models.CharField("nombre de habilidad", max_length=50, unique=True)

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ["name"]

    def __str__(self):
        return self.name


class WorkerSkill(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField("nivel (1-5)", default=1)

    class Meta:
        unique_together = ("worker", "skill")
        verbose_name = "Habilidad del trabajador"
        verbose_name_plural = "Habilidades de trabajadores"

    def __str__(self):
        return f"{self.worker.name} - {self.skill.name} (⭐{self.level})"

class Report(models.Model):
    worker = models.ForeignKey("Worker", on_delete=models.CASCADE, related_name="reports")
    date = models.DateField("fecha", auto_now_add=True)
    performance = models.CharField("desempeño", max_length=100)
    salary = models.DecimalField("salario calculado", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        ordering = ["-date"]

    def __str__(self):
        return f"Reporte de {self.worker.name} ({self.date})"
