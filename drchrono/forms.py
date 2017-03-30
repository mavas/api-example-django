from django import forms


class PatientIdentityForm(forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()
    ssn = forms.CharField()
