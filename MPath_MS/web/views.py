from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
import subprocess
import pymongo
import os

from .forms import SBMLFileForm
from .models import *

from PMGBP.ModelGenerator import ModelGenerator

cl = pymongo.MongoClient()

def index(request):
    return render(request, 'web/index.html')

# Sim-RT-Runner Simulation

def run_simulation(request):
    model = PMGBPModel.objects.get(id=request.GET['model_id'])
    simulation = Simulation(model=model)

    # TODO(Lao): check Celery to handle process
    command = ['sh', './run_simulation.sh', model.name(), simulation.collection()]
    process = subprocess.Popen(command)
    simulation.pid = process.pid
    simulation.save()

    context = {
        'model_name': model.name(),
        'model_id': model.id,
        'simulation_id': simulation.id
    }
    print(context)
    return render(request, 'web/simulation.html', context)

def simulation_results(request):

    simulation = Simulation.objects.get(request.POST['simulation_id'])
    collection = cl.pmgbp[simulation.model.name() + '_' + simulation.model.id + '_' + simulation.id]

    documents = collection.aggregate([
        {
            '$match': {
                'data.log': {'$eq': 'state'},
                'data.state.model_class': {'$eq': 'space'}
            }
        },{
            '$project': {
                'time': '$data.time',
                'metabolites': '$data.state.metabolites'
            }
        },{
            '$unwind': '$metabolites' 
        },{
            '$sort': {'time': 1}
        },{
            '$project': {
                'data': ['$time', '$metabolites.amount'],
                'specie': '$metabolites.id',
            }
        },{
            '$group': {
                '_id': '$specie',
                'specie': {'$first': '$specie'},
                'data': {'$addToSet': '$data'}
             }
        }
    ])
    
    return JsonResponse({'results': [doc for doc in documents]})