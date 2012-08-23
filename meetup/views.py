import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from meetup.models import Flight, Person

DAYS = ['Thursday', 'Friday', 'Saturday']

def home(request):
    data = {}
    flights = data['flights'] = Flight.objects.all().order_by('number')

    arrivals = [{}, {}, {}]

    for flight in flights:
        for person in flight.person_set.all().order_by('id'):
            if flight not in arrivals[person.day]:
                arrivals[person.day][flight] = []
            arrivals[person.day][flight].append(person)

    for day, flights in enumerate(arrivals):
        flights = flights.items()
        flights.sort(key=lambda x: x[0].arrives)
        arrivals[day] = flights

    data['arrivals'] = map(lambda x: (DAYS[x[0]], x[1]), enumerate(arrivals))

    return render_to_response('meetup/home.html', data,
        context_instance=RequestContext(request))

def add(request):
    if 'name' not in request.POST or not request.POST['name']:
        messages.add_message(request, messages.ERROR, 'Must provide a name.')
        return redirect('meetup.views.home')

    person = {
        'name': request.POST['name'],
        'email': request.POST['email'] or None,
        'twitter': request.POST['twitter'] or None,
        'flight': Flight.objects.get(pk=int(request.POST['flight'])),
        'day': int(request.POST['day'] or 1),
    }

    if person['twitter']:
        if person['twitter'].startswith('@'):
            person['twitter'] = person['twitter'][1:]
        elif 'twitter.com' in person['twitter']:
            person['twitter'] = person['twitter'].rsplit('/', 1)[1]

    Person(**person).save()

    return redirect('meetup.views.home')

def robots_txt(request):
    return HttpResponse("User-agent: *\nDisallow: /\n")
