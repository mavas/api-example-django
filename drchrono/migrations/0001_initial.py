# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorSeeAppointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wait_time', models.DateTimeField()),
                ('seen_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('pid', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('appointment', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='doctorseeappointment',
            name='patient',
            field=models.ForeignKey(to='drchrono.Patient'),
        ),
    ]
