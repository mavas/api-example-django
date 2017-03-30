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


def patient_checkin(r):
    c = dict()
    if r.method == 'GET':
        f = PatientCheckinForm()
    elif r.method == 'POST':
        f = PatientCheckinForm(r.POST)
        if f.is_valid():
            access_token = r.user.social_auth.get(provider='drchrono').access_token
            headers = {'Authorization': 'Bearer %s' % access_token}
            params = {'date': date.today(), 'patient': patient_id, 'status': 'Arrived'}
            response = requests.put("%s%s" % (BASE_API_URL, "appointments/%s" % patient_id),
                        params=params,
                        headers=headers,
                        verify=False)
            if response.status_code == 200:
                return redirect('home')
    c['form'] = f
    c = RequestContext(r, c)
    return render_to_response('patient_checkin.html', c)


def oauth2callback(r):
    c = dict()
    if r.method == 'GET':
        f = PatientIdentityForm()
    elif r.method == 'POST':
        print r.POST
        f = PatientIdentityForm(r.POST)
        if f.is_valid():
            fname = f.cleaned_data['fname']
            lname = f.cleaned_data['lname']
            access_token = r.user.social_auth.get(provider='drchrono').access_token
            headers = {'Authorization': 'Bearer %s' % access_token}
            params = {'first_name': fname, 'last_name': lname}
            response = requests.get("%s%s" % (BASE_API_URL, "patients"),
                        params=params,
                        headers=headers,
                        verify=False)
            if response.status_code == 200:
                print response.json()['results']
                return redirect('patient_checkin')
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

    since = date.today() - timedelta(1)
    response = requests.get("%s%s" % (BASE_API_URL, "appointments"),
                params={'since': since},
                headers=headers,
                verify=False)
    c = dict()
    c['appointments'] = response.json()['results']
    c = RequestContext(r, c)
    return render_to_response('doctor.html', c)
