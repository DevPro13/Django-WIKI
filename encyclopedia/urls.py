from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/",views.display_cont,name="display_cont"),
    path("create",views.add,name="add"),
    path("edit/<str:page_title>",views.edit,name="edit"),
    path("update",views.update,name='update'),
    path("random",views.random,name="random"),
]
