from django.db import models


class Patient(models.Model):
    pid = models.CharField(max_length=100, primary_key=True)
    appointment = models.CharField(max_length=100)


class DoctorSeeAppointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    wait_time = models.DateTimeField()
    seen_time = models.DateTimeField()
