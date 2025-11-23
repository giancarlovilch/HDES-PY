# api/serializers.py
from rest_framework import serializers
from schedule.models import Worker, Day, Seat, Skill, WorkerSkill, Report

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]

class WorkerSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = WorkerSkill
        fields = ["id", "skill", "level"]

class WorkerSerializer(serializers.ModelSerializer):
    # usamos la relación intermedia para incluir el nivel (estrellas)
    skills = WorkerSkillSerializer(source="workerskill_set", many=True, read_only=True)

    class Meta:
        model = Worker
        fields = ["id", "name", "created_at", "updated_at", "skills"]

class SeatSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)

    class Meta:
        model = Seat
        fields = ["id", "position", "worker"]

class DaySerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Day
        fields = ["id", "day_of_week", "seats"]

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "date", "performance", "salary", "worker"]


class WorkerProfileSerializer(serializers.ModelSerializer):
    skills = WorkerSkillSerializer(source="workerskill_set", many=True, read_only=True)
    schedule = serializers.SerializerMethodField()
    reports = ReportSerializer(many=True, read_only=True)

    class Meta:
        model = Worker
        fields = ["id", "name", "created_at", "updated_at", "skills", "schedule", "reports"]

    def get_schedule(self, obj):
        seats = obj.seats.select_related("day")
        return [
            {"day": seat.day.get_day_of_week_display(), "position": seat.position}
            for seat in seats
        ]


    
