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
from django.shortcuts import render, render_to_response

from drchrono.forms import PatientIdentityForm


BASE_API_URL = 'https://drchrono.com/api/'
access_token = None


def oauth2callback(r):
    c = dict()
    c['form'] = PatientIdentityForm()
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
