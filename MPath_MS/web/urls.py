from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('simulation', views.run_simulation, name='run_simulation'),
]