from django.db import models
from PMGMP.models import *
# Create your models here.

class Simulation(models.Model):
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    pid = models.IntegerField(null=True, blank=True)
    model = models.ForeignKey(PMGBPModel, on_delete=models.CASCADE)

    def __str__(self):
        if self.end_datetime is not None:
            return self.model.model_name() + " - [" + str(self.start_datetime) + ", " + str(self.end_datetime) + "] - " + str(self.id)
        else:
            return self.model.model_name() + " - " + str(self.start_datetime) + " - " + str(self.id)

    def db_identifier(self):
        return self.model.model_name() + "_" + str(self.id)