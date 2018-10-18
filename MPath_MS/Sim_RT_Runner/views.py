from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse

from django.shortcuts import render
from .tasks import *

# Create your views here.
def run_simulation(request):
	run_simulation_process("/este/es/un/path", "13245")

	return HttpResponseRedirect('/PMGMP/sbml_files')

# Create your views here.
def running_simulation_list(request):
	run_simulation_process("/este/es/un/path", "13245")

	return JsonResponse({'anda': True})