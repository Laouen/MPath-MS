from django.contrib import admin
from django.apps import apps
from PMGMP.models import *

# Register your models here.

for model in apps.get_app_config('PMGMP').models.values():
	admin.site.register(model)