from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse

import os

from .forms import SBMLFileForm
from .models import SBMLfile

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
    os.remove(sbml_file.sbml_model.path)
    sbml_file.delete()
    return JsonResponse({
        'sbml_file_id': request.POST['sbml_file_id'],
        'removed': True
    })

def sbml_files(request):
    sbml_files = [{'id': f.id, 'name': f.filename(), 'url': f.sbml_model.url} for f in SBMLfile.objects.all()]
    return render(request, 'web/sbml_files.html', {'sbml_files': sbml_files})

def generate_model(request):
    sbml_file = SBMLfile.objects.get(id=request.POST['sbml_file_id'])

    model_generator = ModelGenerator(sbml_file.sbml_model.path, 'e', 'p', 'c', json_model=None, groups_size=150)
    model_generator.generate_top()
    model_generator.end_model()
    
    return JsonResponse({
        'sbml_file_id': request.POST['sbml_file_id'],
        'generated': True
    })