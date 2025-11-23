from django.contrib import admin
from .models import Worker, Skill, WorkerSkill, Report, Day, Seat

admin.site.register(Worker)
admin.site.register(Skill)
admin.site.register(WorkerSkill)
admin.site.register(Report)
admin.site.register(Day)
admin.site.register(Seat)
