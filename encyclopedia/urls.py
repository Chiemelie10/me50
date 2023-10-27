from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.display_entry, name="get-entry"),
    path("search", views.search, name="search"),
    path("create/entry", views.create_entry, name="create-entry"),
    path("edit/entry", views.edit_entry, name="edit_entry"),
    path("random/entry", views.display_random_entry, name="get-random-entry")
]
