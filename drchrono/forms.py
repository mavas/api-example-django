from django import forms


class PatientIdentityForm(forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()
    ssn = forms.CharField(required=False)


class PatientCheckinForm(forms.Form):
    GENDERS = (
        ('Female', 'f'),
        ('Male', 'm'),
    )
    LANGUAGES = (
        ('Lojban', 'jbo'),
        ('English', 'en'),
    )
    dob = forms.DateField()
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDERS)
    address_street_first = forms.CharField()
    address_street_second = forms.CharField()
    address_state = forms.CharField(max_length=2)
    address_city = forms.CharField()
    address_zip = forms.CharField()
    preferred_languaget = forms.ChoiceField(choices=LANGUAGES)
