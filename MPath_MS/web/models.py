from django.db import models
from django.core.files.storage import FileSystemStorage

import os

class SBMLfile(models.Model):
    file = models.FileField(upload_to='sbml_files/')
    model_generated = models.BooleanField(default=False)

    def filename(self):
        return os.path.basename(self.file.name)