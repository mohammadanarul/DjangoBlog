import requests
from django.shortcuts import render
from urllib.request import urlopen
import json


def covid_19_Views(request):

    url = "https://covid-193.p.rapidapi.com/statistics"

    querystring = {"country":"Bangladesh"}

    headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "df32b04e82msh4625cf614bd66dfp1fedabjsn0873ffced8f9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    
    d = response['response']
    s = d[0]

    context = {
        'all': s['cases']['total'],
        'recovered': s['cases']['recovered'],
        'deaths': s['deaths']['total'],
        'new_deaths': s['deaths']['new'],
        'new': s['cases']['new'],
        'serioz': s['cases']['critical'],
    }
    print(s)
    return render(request, 'covid19/covid19.html', context)
