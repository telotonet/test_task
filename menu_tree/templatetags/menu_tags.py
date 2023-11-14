from django import template
from django.template.loader import render_to_string
from menu_tree.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu_explicit(context, title=None):
    if title is not None:
        menu_data = MenuItem.get_menu_data(obj_title=str(title))
        if menu_data:
            request = context["request"]
            current_path = request.path
            return render_to_string(
                "menu/draw_menu.html",
                {
                    "query_data": menu_data,
                    "current_path": current_path,
                },
            )
    return ""
