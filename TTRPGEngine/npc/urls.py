from django.urls import path

from . import views

app_name = "npc"

urlpatterns = [
    path('', views.Rooster, name="character-select"),
    path('character', views.character, name="character")
]