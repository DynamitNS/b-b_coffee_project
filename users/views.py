from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegistrationForm, SiteAuthenticationForm


class SiteLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = SiteAuthenticationForm

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        return reverse_lazy('pages:index')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('pages:index')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Регистрация успешно завершена.')
        return redirect('pages:index')

    return render(request, 'users/register.html', {'form': form})
