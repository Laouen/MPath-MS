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
        simulation_process = subprocess.Popen([simulation.model.model.path, simulation.db_identifier()])
        simulation.pid = simulation_process.pid
        simulation.save()
        print("Simulation process started with pid " + str(simulation.pid))