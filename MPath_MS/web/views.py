from django.shortcuts import render, HttpResponseRedirect

from .forms import SBMLFileForm
from .models import SBMLfile


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
            return HttpResponseRedirect('/sbml_list')
        else:
            print('invalid form')

def sbml_files(request):
    sbml_files = [f.sbml_model for f in SBMLfile.objects.all()]
    return render(request, 'web/sbml_files.html', {'sbml_files': sbml_files})
