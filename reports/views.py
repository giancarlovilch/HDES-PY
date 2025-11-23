from django.shortcuts import render

def placeholder_view(request, title):
    return render(request, 'placeholder.html', {'title': title})

def main_view(request):
    return placeholder_view(request, 'Reportes Principales')