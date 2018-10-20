from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from .tasks import *
from .models import *
from PMGMP.models import *
from PMGMP.views import serialize_model

import os
import signal
import json

from pymongo import MongoClient

def serialize_simulation(simulation):
	return {
		'running': simulation.running,
		'id': simulation.id,
		'pid': simulation.pid,
		'db_identifier': simulation.db_identifier(),
		'model': serialize_model(simulation.model)
	}

# Create your views here.
def run_simulation(request, model_id):
	model = PMGBPModel.objects.get(id=model_id)

	simulation = Simulation(model=model, running=False)
	simulation.save()

	run_simulation_process.delay(simulation.id)

	return HttpResponseRedirect('/Sim_RT_Runner/simulation/results/' + str(simulation.id) + '/')

def stop_simulation(request, simulation_id):
	simulation = Simulation.objects.get(id=simulation_id)

	if simulation.pid is not None:
		try:
			print("kill simulation process with PID ", simulation.pid)
			os.kill(simulation.pid, signal.SIGKILL)
		except OSError as ex:
			pass
	
	simulation.end_datetime = timezone.now()
	simulation.running = False
	simulation.save()

	return HttpResponseRedirect('/Sim_RT_Runner/simulation/results/' + str(simulation.id) + '/')

def show_simulation_results(request, simulation_id):
	simulation = Simulation.objects.get(id=simulation_id)

	return render(request, 'Sim_RT_Runner/simulation_results.html', {'simulation': serialize_simulation(simulation)})

def get_simulation_results(request, db_identifier, start_virtual_time):
	client = MongoClient()
	db = client.pmgbp
	ms = eval('db.' + db_identifier)

	col = ms.aggregate([
		{'$match': {
			'data.log': {'$eq': 'state'},
			'data.state.model_class': {'$eq': 'space'},
			'data.time': {'$gt': start_virtual_time}
			}
		}, {'$project': {
			'_id': False,
			'data': True
			}
		}
	])

	return JsonResponse([c for c in col], safe=False)

def running_simulation_list(request):
	running_simulations = Simulation.objects.filter(running=True)

	return render(request, 'Sim_RT_Runner/simulation_list.html', {'simulations': [serialize_simulation(simulation) for simulation in running_simulations]})