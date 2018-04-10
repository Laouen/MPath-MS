from django.db import models
from django.core.files.storage import FileSystemStorage

import os

class SBMLfile(models.Model):
    sbml_model = models.FileField(upload_to='sbml_models/')

    def filename(self):
        return os.path.basename(self.sbml_model.name)