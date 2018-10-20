from django.urls import path

from . import views

urlpatterns = [
    path('run_simulation/<int:model_id>/', views.run_simulation, name='run_simulation'),
    path('stop_simulation/<int:simulation_id>/', views.stop_simulation, name='stop_simulation'),
    path('simulation/results/<int:simulation_id>/', views.show_simulation_results, name='show_simulation_results'),
    path('running_simulation_list/', views.running_simulation_list, name='running_simulation_list'),
    
    # Simulation results
    path('get/simulation_results/', views.get_all_simulation_results, name='get_all_simulation_results'),
]