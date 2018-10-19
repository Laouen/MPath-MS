from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone

from django.shortcuts import render
from .tasks import *
from .models import *
from PMGMP.models import *
from PMGMP.views import serialize_model

import os
import signal

def serialize_simulation(simulation):
	return {
		'id': simulation.id,
		'pid': simulation.pid,
		'model': serialize_model(simulation.model)
	}

# Create your views here.
def run_simulation(request, model_id):
	model = PMGBPModel.objects.get(id=model_id)

	simulation = Simulation(model=model)
	simulation.save()

	run_simulation_process.delay(simulation.id)

	return HttpResponseRedirect('/Sim_RT_Runner/simulation/results/' + str(simulation.id) + '/')

def stop_simulation(request, simulation_id):
	simulation = Simulation.objects.get(id=simulation_id)

	if simulation.pid is not None:
		try:
			print("kill sim", simulation.pid)
			os.kill(simulation.pid, signal.SIGKILL)
		except OSError as ex:
			pass
	
	simulation.end_datetime = timezone.now()
	simulation.save()

	return HttpResponseRedirect('/Sim_RT_Runner/simulation/results/' + str(simulation.id) + '/')

def show_simulation_results(request, simulation_id):
	simulation = Simulation.objects.get(id=simulation_id)

	return render(request, 'Sim_RT_Runner/simulation_results.html', {'simulation': serialize_simulation(simulation)})

def running_simulation_list(request):
	run_simulation_process("/este/es/un/path", "13245")

	return JsonResponse({'anda': True})