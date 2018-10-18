from django.urls import path

from . import views

urlpatterns = [
    path('run_simulation/', views.run_simulation, name='run_simulation'),
    path('running_simulation_list/', views.running_simulation_list, name='running_simulation_list'),
]