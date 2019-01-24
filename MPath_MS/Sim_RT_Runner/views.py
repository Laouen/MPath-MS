from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from .tasks import *
from .models import *
from PMGMP.models import *
from PMGMP.views import serialize_model, serialize_parameter

import os
import signal
import json

from pymongo import MongoClient
from bs4 import BeautifulSoup # sudo pip install beautifulsoup4, lxml

def serialize_simulation(simulation):
	return {
		'running': simulation.running,
		'id': simulation.id,
		'pid': simulation.pid,
		'db_identifier': simulation.db_identifier(),
		'start_datetime': str(simulation.start_datetime),
		'end_datetime': str(simulation.end_datetime),
		'model': serialize_model(simulation.model),
		'parameter': serialize_parameter(simulation.parameter)
	}

def run_simulation(request, model_id, parameter_id):
	model = PMGBPModel.objects.get(id=model_id)
	parameter = Parameter.objects.get(id=parameter_id)

	# Simulation is set as started to be in the running simulation list immediately
	simulation = Simulation(model=model, parameter=parameter, running=True)
	simulation.save()

	run_simulation_process.delay(simulation.id, parameter.id)

	return HttpResponseRedirect('/Sim_RT_Runner/simulation/results/' + str(simulation.id) + '/' + str(parameter.id) + '/')

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

	return HttpResponseRedirect('/Sim_RT_Runner/simulation/results/' + str(simulation.id) + '/' + str(simulation.parameter.id) + '/')

def simulation_list(request):
	running_simulations = Simulation.objects.filter(running=True)
	finished_simulations = Simulation.objects.filter(running=False)

	context_data = {
		'running_simulations': [serialize_simulation(simulation) for simulation in running_simulations],
		'finished_simulations': [serialize_simulation(simulation) for simulation in finished_simulations]
	}

	return render(request, 'Sim_RT_Runner/simulation_list.html', context_data)

def show_simulation_results(request, simulation_id, parameter_id):
	simulation = Simulation.objects.get(id=simulation_id)
	serialized_simulation = serialize_simulation(simulation)

	parameter = Parameter.objects.get(id=parameter_id);
	parameters = BeautifulSoup(open(parameter.file.path, 'r'), 'xml')

	metabolites = []
	for compartmen_metabolites in parameters.find_all("metabolites"):
		metabolites.append({
			'compartment_id': 'space_' + compartmen_metabolites.parent.name,
			'metabolites': [m.attrs['id'] for m in compartmen_metabolites.find_all("metabolite")]
		})

	return render(request, 'Sim_RT_Runner/simulation_results.html', {
		'simulation': serialized_simulation,
		'metabolites': metabolites
	})

@csrf_exempt
def get_all_simulation_results(request):
	
	data = json.loads(request.body.decode('utf-8'))

	client = MongoClient()
	db = client.pmgbp
	ms = eval('db.' + data['db_identifier'])

	pipeline = [
		{'$match': {
			'data.log': {'$eq': 'state'},
			'data.state.model_class': {'$eq': 'space'},
			'data.time': {'$gt': data['start_virtual_time']}
			}
		}, 
		{'$unwind': {'path': '$data.state.metabolites', 'preserveNullAndEmptyArrays': False}},
		{'$project': {
			'_id': False,
			'time': '$data.time',
			'compartment': '$data.model',
			'metabolite': '$data.state.metabolites.id',
			'amount': '$data.state.metabolites.amount'
			}},
		{'$group': {
			'_id': {'metabolite': '$metabolite', 'time': '$time'},
			'compartment': {'$first': '$compartment'},
			'amount': {'$first': '$amount'}
			}
		},
		{'$sort': {'_id.time': 1}},
		{'$group': {
			'_id': '$_id.metabolite',
			'compartment': {'$first': '$compartment'},
			'time': {'$push': '$_id.time'},
			'serie': {'$push': '$amount'}
			}
		},
		{'$project': {
			'_id': False,
			'metabolite': '$_id',
			'compartment': True,
			'data': {'times': '$time', 'serie': '$serie'}
			}
		}
	]

	col = ms.aggregate(pipeline=pipeline, allowDiskUse=True)

	'''
	{'$match': {
			'data.state.metabolites.id': {'$in': ['M_duri_c','M_uLa4n_c','M_dcdp_c','M_actACP_c','M_r5p_c','M_3fe4s_c','M_23dhacoa_c']}
			}},
	'''

	return JsonResponse([c for c in col], safe=False)
