# schedule/management/commands/load_initial_data.py
from django.core.management.base import BaseCommand
from schedule.models import Day, Seat

class Command(BaseCommand):
    help = 'Crea 7 días y 21 asientos (3 por día)'

    def handle(self, *args, **options):
        # Limpiar datos existentes
        Day.objects.all().delete()
        Seat.objects.all().delete()

        # Crear días de la semana
        days_data = [
            {'code': 'Lun', 'name': 'Lunes'},
            {'code': 'Mar', 'name': 'Martes'},
            {'code': 'Mié', 'name': 'Miércoles'},
            {'code': 'Jue', 'name': 'Jueves'},
            {'code': 'Vie', 'name': 'Viernes'},
            {'code': 'Sáb', 'name': 'Sábado'},
            {'code': 'Dom', 'name': 'Domingo'},
        ]
        
        for day_info in days_data:
            day = Day.objects.create(day_of_week=day_info['code'])
            
            # Crear 3 asientos por día
            for position in range(1, 4):
                Seat.objects.create(day=day, position=position)

        self.stdout.write(self.style.SUCCESS('Días y asientos creados correctamente. Ahora puedes agregar trabajadores manualmente.'))