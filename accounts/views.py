from django.shortcuts import render, redirect

def placeholder_view(request, title):
    return render(request, 'placeholder.html', {'title': title})

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('logout')  # O una página de login
    return placeholder_view(request, 'Perfil de Usuario')

def profile_view(request):
    user = request.session.get("user")
    return render(request, "accounts/profile.html", {"user": user})