from django.shortcuts import render

def placeholder_view(request, title):
    return render(request, 'placeholder.html', {'title': title})

def list_view(request):
    return placeholder_view(request, 'Lista de Empleados')

def add_view(request):
    return placeholder_view(request, 'Agregar Empleado')
# Agrega schedule:seat_list si viene de la app original, pero por ahora placeholder
def seat_list_view(request):
    return placeholder_view(request, 'Asignar Horarios (Empleados)')