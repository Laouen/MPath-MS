from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse

import subprocess
import json

from PMGBP.ModelGenerator import ModelGenerator
from PMGBP.SBMLParser import SBMLParserEncoder

from .forms import SBMLFileForm
from .models import *


def serialize_SBMLfile(sbml_file):
    return {
        'id': sbml_file.id,
        'name': sbml_file.filename(),
        'model_generated': sbml_file.model_ready()
    } 

def serialize_parameter(parameter):
    return {
        'id': parameter.id,
        'name': parameter.name()
    }

def serialize_model(model):
    return {
        'id': model.id,
        'name': model.name(),
        'parameters': [serialize_parameter(p) for p in model.parameters.all()]
    }

# Create your views here.
def upload_sbml_form(request):
    if request.method == 'GET':
        return render(request, 'PMGMP/upload_sbml.html')

    if request.method == 'POST':
        print(request.FILES)
        form = SBMLFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/PMGMP/sbml_files')
        else:
            # TODO: Redirect to upload error
            print('invalid form')

def upload_model_parameter(request):
    model_id = request.POST.get('model_id')
    model = PMGBPModel.objects.get(id=model_id)

    parameter = Parameter(file=request.FILES['parameter_file'])
    parameter.save()

    model.parameters.add(parameter)
    model.save()

    return HttpResponseRedirect('/PMGMP/model_files/')

def remove_model_parameter(request, model_id, parameter_id):
    parameter = Parameter.objects.get(id=parameter_id)
    model = PMGBPModel.objects.get(id=model_id)
    
    try:
        os.remove(parameter.file.path)
        
        model.parameters.remove(parameter)
        model.save()
        
        parameter.delete()
    except OSError as e:
        print(e)

    return HttpResponseRedirect('/PMGMP/model_files/')

def sbml_files(request):
    sbml_files = [serialize_SBMLfile(f) for f in SBMLfile.objects.all()]
    return render(request, 'PMGMP/sbml_files.html', {'sbml_files': sbml_files})

def remove_sbml_file(request, sbml_file_id):
    sbml_file = SBMLfile.objects.get(id=sbml_file_id)

    try:
        if not sbml_file.model is None:
            os.remove(sbml_file.model.model.path)
            os.remove(sbml_file.model.parameters.path)
        os.remove(sbml_file.file.path)
    except OSError as e:
        return JsonResponse({
            'sbml_file_id': sbml_file_id,
            'filesystem_error': str(e),
            'removed': False
        })

    sbml_file.delete();

    return JsonResponse({
        'sbml_file_id': sbml_file_id,
        'removed': True
    })

def generate_and_compile_model(request, sbml_file_id):
    sbml_file = SBMLfile.objects.get(id=sbml_file_id)
    model_name = sbml_file.filename().replace('.xml', '')
    sbml_json_file = 'parsed_sbml_datas/' + model_name + '.json'

    try:
        json_model = json.load(open(sbml_json_file, 'r'))
    except Exception as e:
        print(e)
        json_model = None

    # Generate model
    model_generator = ModelGenerator(sbml_file.file.path,
                                     'e',
                                     'p',
                                     'c',
                                     model_dir='./PMGBP',
                                     json_model=json_model,
                                     groups_size=150)

    # Save the parsed data for later reuse
    if not os.path.isfile(sbml_json_file):
        try:
            json.dump(model_generator.parser, open(sbml_json_file, 'w+'), cls=SBMLParserEncoder, indent=4)
        except Exception as e:
            print(e)

    model_generator.generate_top()
    model_generator.end_model()


    # Compile model
    completed_process = subprocess.run(["sh", "./compile_model.sh", model_name])

    # Save model in Django
    if completed_process.returncode == 0:
        pmgbp_model = PMGBPModel()
        pmgbp_model.model.name = 'compiled_models/' + model_name
        pmgbp_model.save()

        sbml_file.model = pmgbp_model
        sbml_file.save()

        model_parameter = Parameter()
        model_parameter.file.name = 'model_parameters/' + model_name + '.xml'
        model_parameter.save() 
        pmgbp_model.parameters.add(model_parameter)

        return JsonResponse({
            'sbml_file_id': sbml_file_id,
            'model_id': pmgbp_model.id,
            'return_code': completed_process.returncode
        })
    else:
        return JsonResponse({
            'sbml_file_id': sbml_file_id,
            'retur_ncode': completed_process.returncode
        })

def model_files(request):
    model_files = [serialize_model(m) for m in PMGBPModel.objects.all()]
    return render(request, 'PMGMP/model_files.html', {'model_files': model_files})

def remove_model(request, model_id):
    pmgbp_model = PMGBPModel.objects.get(id=model_id)
    sbml_json_file = 'parsed_sbml_datas/' + pmgbp_model.model_name() + '.json'

    try:
        os.remove(pmgbp_model.model.path)

        try:
            for parameter in pmgbp_model.parameters.all():
                os.remove(parameter.file.path)
                parameter.delete()

            os.remove(sbml_json_file)
        except OSError as e:
            print(e)

    except OSError as e:
        return JsonResponse({
            'model_id': model_id,
            'filesystem_error': str(e),
            'removed': False
        })

    pmgbp_model.delete()
    return JsonResponse({
        'model_id': model_id,
        'removed': True
    })
