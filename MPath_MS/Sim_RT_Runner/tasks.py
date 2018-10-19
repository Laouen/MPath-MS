from __future__ import absolute_import
from celery import shared_task

import subprocess

from Sim_RT_Runner.models import *

@shared_task  # Use this decorator to make this a asyncronous function
def run_simulation_process(simulation_id):
    
    simulation = Simulation.objects.get(id=simulation_id)

    if simulation.end_datetime is not None:
        print("Simulation was stopped before starting")
    else:

        print("Start simulation process")
        print(' '.join([simulation.model.model.path, './model_parameters/' + simulation.model.model_name() + '.xml', simulation.db_identifier()]))
        simulation_process = subprocess.Popen([simulation.model.model.path, './model_parameters/' + simulation.model.model_name() + '.xml', simulation.db_identifier()])
        simulation.pid = simulation_process.pid
        simulation.save()
        print("Simulation process started with pid " + str(simulation.pid))