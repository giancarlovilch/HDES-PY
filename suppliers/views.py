from django.shortcuts import render

def placeholder_view(request, title):
    return render(request, 'placeholder.html', {'title': title})

def list_view(request):
    return placeholder_view(request, 'Lista de Proveedores')