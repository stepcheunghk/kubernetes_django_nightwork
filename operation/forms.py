from django import forms
from .models import Operation, SpecialDate
import datetime

STAFF=[
    ('Roger Liu', 'Roger Liu'),
    ('Teddy Kwong', 'Teddy Kwong'),
    ('Rick Ching', 'Rick Ching'),
    ('David Lun', 'David Lun'),
    ('Matt So', 'Matt So'),
    ('Nancy Nie', 'Nancy Nie'),
    ('Leo Liu', 'Leo Liu'),
    ('Stephen Cheung', 'Stephen Cheung'),
    ('Billy Chan', 'Billy Chan'),
]

DOMAIN=[
    ('NFV', 'NFV'),
    ('Private Cloud', 'Private Cloud'),
    ('Smartcare', 'Smartcare'),
    ('Other', 'Other'),
]

CATEGORY=[
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
]

LOCATION=[
    ('MITA', 'MITA'),
    ('GNC', 'GNC'),
    ('KCC', 'KCC'),
    ('Remote', 'Remote'),
]

SPECIALDATE=[
    ('Chinese New Year', 'Chinese New Year'),
    ('Ching Ming', 'Ching Ming'),
    ('Buddha Birthday', 'Buddha Birthday'),
    ('Dragon Boat', 'Dragon Boat'),
    ('Mid Autumn', 'Mid Autumn'),
    ('Chung Yeung', 'Chung Yeung'),
    ('CMHK Half Day', 'CMHK Half Day'),
    ('Frozen', 'Frozen'),
]

REASONTYPE=[
    ('Configuration Change', 'Configuration Change'),
    ('Preventive Maintenance', 'Preventive Maintenance'),
    ('H/W upgrade', 'H/W upgrade'),
    ('S/W upgrade', 'S/W upgrade'),
    ('Expansion', 'Expansion'),
    ('Fault Solution', 'Fault Solution'),
    ('Partner Network Maintenance', 'Partner Network Maintenance'),
    ('Facility Maintenance', 'Facility Maintenance'), 
]

class OperationForm (forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            'name',
            'phone',
            'domain',
            'category',
            'startdate',
            'starttime',
            'enddate',
            'endtime',
            'location',
            'subject',
            'reason_type',
            'reason',
            'impact',
            'remarks',
            'vendor',
            'vendor_phone',
            'mop',
        ]
        widgets = {
            'name': forms.Select(choices=STAFF),
            'domain': forms.Select(choices=DOMAIN),
            'category': forms.Select(choices=CATEGORY),
            'location': forms.Select(choices=LOCATION),
            'reason_type': forms.Select(choices=REASONTYPE),
            'subject': forms.Textarea(attrs={'rows':1, 'cols': 100, 'style':'resize:none;'}),
            'reason': forms.Textarea(attrs={'rows':1, 'cols': 100, 'style':'resize:none;'}),
            'impact': forms.Textarea(attrs={'rows':1, 'cols': 100, 'style':'resize:none;'})
        }

class DateInput(forms.DateInput):
    input_type  = 'Date'

class TimeInput(forms.TimeInput):
    input_type  = 'Time'
    input_formats = "%H:%i"
 
class RawOperationForm (forms.Form):
    name            = forms.ChoiceField(widget=forms.Select, choices=STAFF)
    phone           = forms.CharField()
    domain          = forms.ChoiceField(widget=forms.Select, choices=DOMAIN)
    category        = forms.ChoiceField(widget=forms.Select, choices=CATEGORY, initial='D')
    startdate       = forms.DateField(widget=DateInput)
    starttime       = forms.TimeField(widget=TimeInput, initial=datetime.time(00,00))
    enddate         = forms.DateField(widget=DateInput)
    endtime         = forms.TimeField(widget=TimeInput, initial=datetime.time(6,00))
    location        = forms.ChoiceField(widget=forms.Select, choices=LOCATION)
    subject         = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'e.g. CMHK GNC Core V5 Host Expansion','size':'60'}))
    reason_type     = forms.ChoiceField(widget=forms.Select, choices=REASONTYPE)
    reason          = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. Private Cloud hardware expansion', 'size':'60'}))
    impact          = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}))
    remarks         = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':'60'}))
    vendor          = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. ZhangXXXXXXXX'}))
    vendor_phone    = forms.CharField(required=False)
    mop             = forms.FileField(required=False)

class SpecialDateForm (forms.Form):
    name = forms.ChoiceField(widget=forms.Select, choices=SPECIALDATE)
    startdate = forms.DateField(widget=DateInput)
    enddate = forms.DateField(widget=DateInput)