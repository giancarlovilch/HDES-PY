import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from schedule.models import Worker, Skill, WorkerSkill, Report
from .serializers import WorkerSerializer, DaySerializer, SkillSerializer, WorkerProfileSerializer, ReportSerializer


@api_view(["GET"])
def employees_list(request):
    empleados = Worker.objects.all()
    serializer = WorkerSerializer(empleados, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def schedule_list(request):
    days = Day.objects.prefetch_related("seats__worker").all()
    serializer = DaySerializer(days, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def skills_list(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def worker_profile(request, worker_id):
    try:
        worker = Worker.objects.get(id=worker_id)
        serializer = WorkerProfileSerializer(worker)
        return Response(serializer.data)
    except Worker.DoesNotExist:
        return Response({"error": "Trabajador no encontrado"}, status=404)


@api_view(["POST"])
def assign_skill(request):
    """
    Espera un JSON:
    {
      "worker_id": 1,
      "skill_id": 2,
      "level": 3
    }
    """
    worker_id = request.data.get("worker_id")
    skill_id = request.data.get("skill_id")
    level = request.data.get("level", 1)

    try:
        worker = Worker.objects.get(id=worker_id)
        skill = Skill.objects.get(id=skill_id)

        obj, created = WorkerSkill.objects.update_or_create(
            worker=worker, skill=skill,
            defaults={"level": level}
        )

        return Response({
            "message": f"Skill {skill.name} asignada a {worker.name} con nivel {level}",
            "created": created
        })
    except Worker.DoesNotExist:
        return Response({"error": "Trabajador no encontrado"}, status=404)
    except Skill.DoesNotExist:
        return Response({"error": "Skill no encontrada"}, status=404)


@api_view(["GET", "POST"])
def reports_list(request):
    if request.method == "GET":
        reports = Report.objects.select_related("worker").all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == "GET":
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        report.delete()
        return Response({"message": "Reporte eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def php_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # URL de tu API PHP
    url = "http://localhost:3000/myphp/api_login.php"

    try:
        response = requests.post(url, json={"username": username, "password": password})
        data = response.json()
    except Exception as e:
        return Response({"error": "No se pudo conectar al API PHP", "detail": str(e)}, status=500)

    if data.get("success"):
        # Guardar en la sesión de Django
        request.session["user"] = data["user"]
        request.session["token"] = data["token"]
        return Response({"message": "Login exitoso", "user": data["user"]})
    else:
        return Response({"message": "Credenciales inválidas"}, status=401)
