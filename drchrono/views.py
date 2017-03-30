import os
import logging
import httplib2

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from drchrono.forms import PatientIdentityForm


def oauth2callback(r):
    d = dict()
    d['form'] = PatientIdentityForm()
    return render_to_response('patient.html', d)


def home(r):
    return render_to_response('index.html', {})


def doctor(r):
    return render_to_response('index.html', {})
