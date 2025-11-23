from django.shortcuts import render

def placeholder_view(request, title):
    return render(request, 'placeholder.html', {'title': title})

def list_view(request):
    return placeholder_view(request, 'Lista de Inventario')

def add_view(request):
    return placeholder_view(request, 'Agregar Producto')

def manage_view(request):
    return placeholder_view(request, 'Gestionar Categorías')