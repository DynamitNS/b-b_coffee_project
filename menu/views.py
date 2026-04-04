"""Вьюхи для страницы меню"""
from django.db.models import Q, Prefetch
from django.views.generic import TemplateView

from .models import Category, MenuItem


class MenuView(TemplateView):
    """Страница меню с поиском, фильтрацией и группировкой по категориям"""
    template_name = 'menu/menu.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        query = (self.request.GET.get('q') or '').strip()
        category_slug = (self.request.GET.get('category') or '').strip()

        items = MenuItem.objects.select_related('category').filter(is_available=True)

        if query:
            items = items.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
            )

        if category_slug:
            items = items.filter(category__slug=category_slug)

        items = items.order_by('category__order', 'order', 'name')

        categories = Category.objects.order_by('order', 'name').prefetch_related(
            Prefetch('items', queryset=items, to_attr='visible_items')
        )

        categories = [cat for cat in categories if getattr(cat, 'visible_items', [])]

        ctx.update({
            'categories': categories,
            'query': query,
            'selected_category': category_slug,
            'all_categories': Category.objects.order_by('order', 'name'),
        })
        return ctx
