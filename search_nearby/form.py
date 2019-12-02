from django import forms

Option_Type = [
    ('0', 'Light Conditions'),
    ('1', 'Road Surface Conditions'),
    ('2', 'Road Type'),
    ('3', 'Weather Conditions'),
    ('4', 'Year'),
]
cities_opt = [
    ('London', 'London'),
    
]

class opsi_filter(forms.Form):
    lon=forms.CharField()
    lat =forms.CharField()
    # cities = forms.CharField( widget=forms.Select(choices=cities_opt))
    radius = forms.CharField()
    limit = forms.CharField()
    filter_type= forms.CharField( widget=forms.Select(choices=Option_Type))
