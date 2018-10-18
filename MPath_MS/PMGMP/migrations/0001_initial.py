# Generated by Django 2.0.4 on 2018-10-18 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PMGBPModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.FileField(upload_to='compiled_models/')),
                ('parameters', models.FileField(upload_to='model_parameters/')),
            ],
        ),
        migrations.CreateModel(
            name='SBMLfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='sbml_files/')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='PMGMP.PMGBPModel')),
            ],
        ),
    ]