from django import forms


#class AppointmentSelectionForm(forms.Form):
#    appointments = forms.ChoiceField(


class PatientIdentityForm(forms.Form):
    fname = forms.CharField(label='First name')
    lname = forms.CharField(label='Last name')
    ssn = forms.CharField(label='Social security number', required=False)


class PatientCheckinForm(forms.Form):
    GENDERS = (
        ('Female', 'f'),
        ('Male', 'm'),
    )
    LANGUAGES = (
        ('Lojban', 'jbo'),
        ('English', 'en'),
    )
    dob = forms.DateField(required=False)
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDERS)
    address_street_first = forms.CharField()
    address_street_second = forms.CharField(required=False)
    address_state = forms.CharField(max_length=2)
    address_city = forms.CharField()
    address_zip = forms.CharField()
    preferred_languaget = forms.ChoiceField(choices=LANGUAGES)
