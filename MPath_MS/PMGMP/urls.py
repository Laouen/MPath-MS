from django.urls import path

from . import views

urlpatterns = [
    path('upload_sbml_file/', views.upload_sbml_form, name='upload_sbml_form'),
    path('upload_model_parameter/', views.upload_model_parameter, name='upload_model_parameter'),
    path('sbml_files/', views.sbml_files, name='sbml_files'),
    path('remove_sbml_file/<int:sbml_file_id>/', views.remove_sbml_file, name='remove_sbml_file'),
    path('remove_model_parameter/<int:model_id>/<int:parameter_id>/', views.remove_model_parameter, name='remove_model_parameter'),
    path('generate_and_compile_model/<int:sbml_file_id>/', views.generate_and_compile_model, name='generate_and_compile_model'),
    path('model_files/', views.model_files, name='model_files'),
    path('remove_model/<int:model_id>/', views.remove_model, name='remove_model'),
]