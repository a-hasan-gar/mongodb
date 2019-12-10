from django import forms

Option_Type = [
    ('0', 'Light Conditions'),
    ('1', 'Road Surface Conditions'),
    ('2', 'Road Type'),
    ('3', 'Weather Conditions'),
    ('4', 'Year'),
]
cities_opt = [
    ('lon=-0.1278&lat=51.5074', 'London'),
    ('lon=-2.2426&lat=53.4808', 'Manchester'),
    ('lon=-1.8904&lat=52.4862', 'Birmingham'),
    ('lon=-1.5491&lat=53.8008', 'Leeds'),
    ('lon=-4.2518&lat=55.8642', 'Glasgow'),
    ('lon=-2.9916&lat=53.4084', 'Liverpool'),
    ('lon=-1.4044&lat=50.9097', 'Southampton'),
    ('lon=-1.6178&lat=54.9783', 'Newcastle'),
    ('lon=-1.1581&lat=52.9548', 'Nottingham'),
    ('lon=-1.4701&lat=53.3811', 'Sheffield'),
    ('lon=-2.5879&lat=51.4545', 'Bristol'),
    ('lon=-1.1398&lat=52.6369', 'Leicester'),
    ('lon=-3.1883&lat=55.9533', 'Edinburgh'),
    ('lon=-5.9301&lat=54.5973', 'Belfast'),
    ('lon=-0.1372&lat=50.8225', 'Brighton'),
    ('lon=-1.8808&lat=50.7192', 'Bournemouth'),
    ('lon=-3.1791&lat=51.4816', 'Cardiff'),
    ('lon=-1.2350&lat=54.5742', 'Middlesbrough'),
    ('lon=-2.1794&lat=53.0027', 'Stoke-on-Trent'),
    ('lon=-1.5197&lat=52.4068', 'Coventry'),
    
]

class opsi_filter(forms.Form):
    lat_lon=forms.CharField()
    # lat =forms.CharField()
    # cities = forms.CharField( widget=forms.Select(choices=cities_opt))
    radius = forms.CharField()
    limit = forms.CharField()
    filter_type= forms.CharField( widget=forms.Select(choices=Option_Type))
