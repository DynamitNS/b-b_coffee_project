"""Вьюха для страницы контактов и бронирования"""
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ReservationForm


class ContactView(FormView):
    """Страница контактов с формой бронирования"""
    template_name = 'orders/contacts.html'
    form_class = ReservationForm
    success_url = reverse_lazy('orders:contacts')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Флаг успешной отправки при редиректе
        ctx['success'] = self.request.GET.get('ok') == '1'
        return ctx

    def get_success_url(self):
        return reverse_lazy('orders:contacts') + '?ok=1'
