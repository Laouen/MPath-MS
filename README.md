# MPath-MS
A Django web platform for Modelling and simulation of Metabolic pathways


# Celery installation guide
https://medium.com/@ffreitasalves/executing-time-consuming-tasks-asynchronously-with-django-and-celery-8578eebab356

# How to start server
1. create virtualenv and intall dependencies
2. sudo systemctl start mongod.service
2. sudo systemctl start postgresql.service
3. open 2 terminals in the project root and start the project virtualenv each terminal
4. in terminal 1 do: 
	1. cd MPath_MS/
	2. celery --app=MPath_MS worker --loglevel=INFO
5. in terminal 2 do:
	1. cd MPath_MS/
	2. python manage.py runserver 