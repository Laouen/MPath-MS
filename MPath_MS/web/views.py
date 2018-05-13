from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
import subprocess

import os

from .forms import SBMLFileForm
from .models import *

from PMGBP.ModelGenerator import ModelGenerator


def index(request):
    return render(request, 'web/index.html')

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
        os.remove(sbml_file.file.path)
    except:
        pass
    sbml_file.delete()
    return JsonResponse({
        'sbml_file_id': request.POST['sbml_file_id'],
        'removed': True
    })

def sbml_files(request):
    sbml_files = [{'id': f.id, 'name': f.filename(), 'model_generated': f.model_generated} for f in SBMLfile.objects.all()]
    return render(request, 'web/sbml_files.html', {'sbml_files': sbml_files})

def generate_model(request):
    sbml_file = SBMLfile.objects.get(id=request.POST['sbml_file_id'])

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


    # compile model
    completed_process = subprocess.run(["sh", "./compile_model.sh", model_name])

    pmgbp_model = PMGBPModel(sbml_file=sbml_file)
    pmgbp_model.model.name = 'compiled_models/' + model_name
    pmgbp_model.parameters.name = 'model_parameters/' + model_name + '.xml'
    pmgbp_model.save()

    sbml_file.model_generated = True
    sbml_file.save()
    return JsonResponse({
        'sbml_file_id': request.POST['sbml_file_id'],
        'generated': True
        #'compiled': completed_process.returncode
    })