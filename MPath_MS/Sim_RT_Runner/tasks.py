from __future__ import absolute_import
from celery import shared_task

@shared_task  # Use this decorator to make this a asyncronous function
def run_simulation_process(model_path, simulation_id):
    print("Asynchronous task")
    print(model_path)
    print(simulation_id)