from django.shortcuts import render, redirect
from django.urls import reverse
from myapp.parts.user_register_form import UserRegistrationForm
import traceback

def user_register_view(request):
    try:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('login'))
        else:
            form = UserRegistrationForm()
    except Exception as e:
        print(traceback.format_exc())
        form = UserRegistrationForm()
    return render(request, 'user_register.html', {'form': form})