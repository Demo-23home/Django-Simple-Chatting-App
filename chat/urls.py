from django.urls import path
from . import views

urlpatterns = [
    path("new_group", views.create_group, name="new_group"),
    path("join_group/<uuid:uuid>", views.join_group, name="join_group"),
    path("leave_group/<uuid:uuid>", views.leave_group, name="leave_group"),
    path("remove_group/<uuid:uuid>", views.delete_group, name="remove_group"),
    path("open_chat/<uuid:uuid>", views.open_chat, name="open_chat"),
]
