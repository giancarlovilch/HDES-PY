from django.shortcuts import render

def placeholder_view(request, title):
    return render(request, 'placeholder.html', {'title': title})

def privacy_view(request):
    return placeholder_view(request, 'Política de Privacidad')

def terms_view(request):
    return placeholder_view(request, 'Términos de Servicio')