from django.shortcuts import redirect
from django.urls import reverse
from schedule.models import Worker


class PHPAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_php = request.session.get("user")

        allowed_paths = [
            reverse("php_login_form"),
            "/admin/",
            "/api/",  
            "/sso/"    
        ]
        
        if not request.user_php and not any(request.path.startswith(p) for p in allowed_paths):
            return None  
       
        # Crear Worker automático si no existe
        if request.user_php:
            nickname = request.user_php.get("nickname") or request.user_php.get("id")
            if nickname:
                worker, created = Worker.objects.get_or_create(name=nickname)
                request.worker = worker
        else:
            request.worker = None
        # ---------------

        return self.get_response(request)

