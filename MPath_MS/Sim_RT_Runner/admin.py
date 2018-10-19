from django.contrib import admin
from django.apps import apps
from Sim_RT_Runner.models import *

# Register your models here.

for model in apps.get_app_config('Sim_RT_Runner').models.values():
	admin.site.register(model)