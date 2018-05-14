from django.db import models
from django.core.files.storage import FileSystemStorage

import os

class SBMLfile(models.Model):
    file = models.FileField(upload_to='sbml_files/')
    model = models.ForeignKey('PMGBPModel', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.filename().replace('.xml', '')

    def filename(self):
        return os.path.basename(self.file.name)

    def model_ready(self):
        return not self.model is None

class PMGBPModel(models.Model):
    model = models.FileField(upload_to='compiled_models/')
    parameters = models.FileField(upload_to='model_parameters/')

    def delete(self):
        for sbml_file in SBMLfile.objects.filter(model=self):
            sbml_file.model = None
            sbml_file.save()
        models.Model.delete(self)

    def __str__(self):
        return self.name()

    def name(self):
        return os.path.basename(self.model.path)

class Simulation(models.Model):
    model = models.ForeignKey('PMGBPModel', on_delete=models.DO_NOTHING)
    pid = models.IntegerField(null=True, blank=True)

    def collection(self):
        return '_'.join([self.model.name(), self.model.id, self.id])