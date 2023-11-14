from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from .models import MenuItem


class MenuItemDetailView(View):
    template_name = "menu.html"

    def get(self, request, *args, **kwargs):
        path = kwargs.get("path")
        menu_item = get_object_or_404(MenuItem, path=path)
        return render(request, self.template_name, {"title": menu_item.title})


class MainMenuView(ListView):
    template_name = "main_page.html"
    model = MenuItem
    queryset = model.objects.filter(parent_id__isnull=True)
    context_object_name = "list"
