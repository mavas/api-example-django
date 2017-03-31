import os
import logging
import httplib2
import datetime
from datetime import timedelta, date

import requests
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect

from drchrono.forms import PatientIdentityForm, PatientCheckinForm


BASE_API_URL = 'https://drchrono.com/api/'
access_token = None


def select_appointment(r, patient_id):
    """Allows a patient to select one of many appointments."""
    c = dict()

    if r.method == 'POST':
        if 'appointment' in r.POST:
            appointment_id = r.POST['appointment']
            return redirect('patient_checkin', appointment_id=appointment_id)

    access_token = r.user.social_auth.get(provider='drchrono').access_token
    headers = {'Authorization': 'Bearer %s' % access_token}
    params = {'patient': patient_id, 'date': date.today()}
    response = requests.get("%s%s" % (BASE_API_URL, "appointments"),
                params=params, headers=headers, verify=False)
    if response.status_code == 200:
        results = response.json()['results']
        c['appointments'] = []
        for result in results:
            if result['status'] != 'Arrived':
                c['appointments'].append(result)
        c['patient_id'] = patient_id
    c = RequestContext(r, c)
    return render_to_response('select_appointment.html', c)


def patient_checkin(r, appointment_id):
    """The screen that checks a patient in.

    This screen is representative of a customer/patient walking in to a
    doctor's office.  They go to the front desk to tell the clerk that they are
    there for their appointment, and the clerk gives them a sheet of
    information to fill out in the meantime while the doctor comes on their
    way.  This page is that sheet.  Once they fill out the information and give
    it back to the clerk - after they click 'Submit' - their appointment in the
    database is marked as 'Arrived'.
    """
    c = dict()

    if r.method == 'GET':
        f = PatientCheckinForm()

    elif r.method == 'POST':
        f = PatientCheckinForm(r.POST)
        if f.is_valid():
            # Update the API endpoint with a status of 'Arrived'.
            access_token = r.user.social_auth.get(provider='drchrono').access_token
            headers = {'Authorization': 'Bearer %s' % access_token}
            params = {'status': 'Arrived'}
            response = requests.patch(
                        "%s%s" % (BASE_API_URL, "appointments/%s" % appointment_id),
                        data=params,
                        headers=headers,
                        verify=False)

            # Update the database with the status.
            if response.status_code == 204:
                return redirect('patient_home')

    c['form'] = f
    c['appointment'] = appointment_id
    c = RequestContext(r, c)
    return render_to_response('patient_checkin.html', c)


def patient_home(r):
    """The patient's home page."""
    c = dict()

    if r.method == 'GET':
        f = PatientIdentityForm()

    elif r.method == 'POST':
        f = PatientIdentityForm(r.POST)

        # If the form is valid, we check if the data refers to an
        # existing/actual patient.
        if f.is_valid():
            fname = f.cleaned_data['fname']
            lname = f.cleaned_data['lname']
            access_token = r.user.social_auth.get(provider='drchrono').access_token
            headers = {'Authorization': 'Bearer %s' % access_token}
            params = {'first_name': fname, 'last_name': lname}
            response = requests.get("%s%s" % (BASE_API_URL, "patients"),
                        params=params, headers=headers, verify=False)
            # The patient exists.
            if response.status_code == 200:
                patient_id = response.json()['results'][0]['id']
                params = {'patient': patient_id, 'date': date.today()}
                response = requests.get("%s%s" % (BASE_API_URL, "appointments"),
                            params=params, headers=headers, verify=False)
                if response.status_code == 200:
                    results = response.json()['results']
                    if len(results) == 1:
                        appointment_id = results[0]['id']
                        return redirect('patient_checkin', appointment_id=appointment_id)
                    elif len(results) > 1:
                        return redirect('select_appointment', patient_id=patient_id)
                    else:
                        print("Warning!")
            else:
                print("Could not retrieve data on %s %s" % (fname, lname))
                print response.reason
        else:
            print "Form not valid."

    c['form'] = f
    c = RequestContext(r, c)
    return render_to_response('patient.html', c)


def home(r):
    return render_to_response('index.html', {})


def doctor(r):
    access_token = r.user.social_auth.get(provider='drchrono').access_token
    headers = {'Authorization': 'Bearer %s' % access_token}

    response = requests.get("%s%s" % (BASE_API_URL, "appointments"),
                params={'date': date.today()},
                headers=headers,
                verify=False)
    c = dict()
    c['appointments'] = response.json()['results']
    c['appointments_checked_in'] = []
    for a in c['appointments']:
        if a['status'] == 'Arrived':
            waiting_time = str(datetime.datetime.now()) + ' - ' + a['scheduled_time']
            c['appointments_checked_in'].append((a, waiting_time))
    def compute_this():
        r = 'david'
        return r
    c['overall_avg_wait_time'] = compute_this()
    c = RequestContext(r, c)
    return render_to_response('doctor.html', c)
