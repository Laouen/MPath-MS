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

# SBML file views

def upload_sbml_form(request):
    if request.method == 'GET':
        return render(request, 'web/upload_sbml.html')

    if request.method == 'POST':
        print(request.FILES)
        form = SBMLFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('save file')
            form.save()
            return HttpResponseRedirect('/sbml_files')
        else:
            print('invalid form')

def remove_sbml_file(request):
    sbml_file = SBMLfile.objects.get(id=request.POST['sbml_file_id'])

    try:
        if not sbml_file.model is None:
            os.remove(sbml_file.model.model.path)
            os.remove(sbml_file.model.parameters.path)
            sbml_file.model.delete()
        os.remove(sbml_file.file.path)
    except OSError as e:
        return JsonResponse({
            'sbml_file_id': request.POST['sbml_file_id'],
            'filesystem_error': str(e),
            'removed': False
        })

    sbml_file.delete()
    return JsonResponse({
        'sbml_file_id': request.POST['sbml_file_id'],
        'removed': True
    })

def sbml_files(request):
    sbml_files = [{'id': f.id, 'name': f.filename(), 'model_generated': f.model_ready()} for f in SBMLfile.objects.all()]
    return render(request, 'web/sbml_files.html', {'sbml_files': sbml_files})

def generate_model(request):
    sbml_file = SBMLfile.objects.get(id=request.POST['sbml_file_id'])

    # Generate model
    model_name = sbml_file.filename().replace('.xml', '')
    model_generator = ModelGenerator(sbml_file.file.path,
                                     'e',
                                     'p',
                                     'c',
                                     model_dir='./PMGBP',
                                     parameters_path='../model_parameters/' + model_name + '.xml',
                                     json_model=None,
                                     groups_size=150)
    model_generator.generate_top()
    model_generator.end_model()


    # Compile model
    completed_process = subprocess.run(["sh", "./compile_model.sh", model_name])

    # Save model in Django
    if completed_process.returncode == 0:
        pmgbp_model = PMGBPModel()
        pmgbp_model.model.name = 'compiled_models/' + model_name
        pmgbp_model.parameters.name = 'model_parameters/' + model_name + '.xml'
        pmgbp_model.save()

        sbml_file.model = pmgbp_model
        sbml_file.save()

        return JsonResponse({
            'sbml_file_id': request.POST['sbml_file_id'],
            'model_id': pmgbp_model.id,
            'return_code': completed_process.returncode
        })
    else:
        return JsonResponse({
            'sbml_file_id': request.POST['sbml_file_id'],
            'retur_ncode': completed_process.returncode
        })

# Models views

def model_files(request):
    model_files = [{'id': m.id, 'name': m.name()} for m in PMGBPModel.objects.all()]
    return render(request, 'web/model_files.html', {'model_files': model_files})

def remove_model(request):
    pmgbp_model = PMGBPModel.objects.get(id=request.POST['model_id'])

    try:
        os.remove(pmgbp_model.model.path)
        os.remove(pmgbp_model.parameters.path)
    except OSError as e:
        return JsonResponse({
            'model_id': request.POST['model_id'],
            'filesystem_error': str(e),
            'removed': False
        })

    pmgbp_model.delete()
    return JsonResponse({
        'model_id': request.POST['model_id'],
        'removed': True
    })

# Simulation

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