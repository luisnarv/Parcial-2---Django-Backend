from django.urls import path
from .views import ProyectoView

urlpatterns = [
    path('proyectos/', ProyectoView.as_view()),
    path('proyectos/<int:pk>/', ProyectoView.as_view()),
]
