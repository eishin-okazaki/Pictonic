from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
            allowed_paths = [reverse('register'), reverse('login')] 
            if not request.user.is_authenticated:
                if request.path not in allowed_paths:
                    return redirect('login')
            return None
