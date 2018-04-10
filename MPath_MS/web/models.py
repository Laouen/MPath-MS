from django.db import models

class SBMLfile(models.Model):
    sbml_model = models.FileField(upload_to='sbml_models/')