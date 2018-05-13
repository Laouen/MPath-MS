from django.db import models
from django.core.files.storage import FileSystemStorage

import os

class SBMLfile(models.Model):
    file = models.FileField(upload_to='sbml_files/')
    model_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.filename().replace('.xml', '') + ' - ' + 'model ready: ' + str(self.model_generated)

    def filename(self):
        return os.path.basename(self.file.name)

class PMGBPModel(models.Model):
    model = models.FileField(upload_to='compiled_models/')
    parameters = models.FileField(upload_to='model_parameters/')
    sbml_file = models.ForeignKey('SBMLfile', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.sbml_file.filename().replace('.xml', '')

    def filename(self):
        return os.path.basename(self.file.name)