from django.urls import path, re_path
from .views import MainMenuView, MenuItemDetailView

urlpatterns = [
    path("", MainMenuView.as_view(), name="menu"),
    re_path(r"^item/(?P<path>.*)/$", MenuItemDetailView.as_view(), name="detail"),
]
