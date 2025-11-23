from django.shortcuts import render

def placeholder_view(request, title):
    return render(request, 'placeholder.html', {'title': title})

def register_view(request):
    return placeholder_view(request, 'Registrar Venta')

def reports_view(request):
    return placeholder_view(request, 'Reportes de Ventas')

def history_view(request):
    return placeholder_view(request, 'Historial de Ventas')