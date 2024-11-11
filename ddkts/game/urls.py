from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("play", views.play, name="play"),
    path("question", views.question, name="question"),
    path("answer", views.answer, name="answer"),
]
