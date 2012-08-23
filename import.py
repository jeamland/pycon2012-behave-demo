import csv
import datetime

import dateutil.tz

from meetup.models import Flight

# JQXXX -> QF5XXX
# DJXXX -> VAXXX

EST = dateutil.tz.gettz('Australia/Hobart')

terminals = {
    'Jetstar Airways': 'Qantas/Jetstar',
    'Qantas Airways': 'Qantas/Jetstar',
    'Virgin Australia': 'Virgin/International',
}

friday = datetime.date(2012, 8, 17)

data = csv.DictReader(open('hba-flights.csv'))
for row in data:
    carrier = row['AIRLINE']
    hour, minute, second = [int(x) for x in row['SCHEDULED ARRIVAL'].split(':')]

    arrival = datetime.time(hour=hour, minute=minute, second=second)
    arrival = datetime.datetime.combine(friday, arrival)
    arrival = arrival.replace(tzinfo=EST)

    flight = {
        'origin': row['ORIGIN'].split(' ', 1)[1],
        'number': row['FLIGHT NUMBER'],
        'terminal': terminals[carrier],
        'carrier': carrier,
        'arrives': arrival,
    }

    if flight['number'].startswith('JQ'):
        number = flight['number'].split(' ')[1]
        flight['code_share'] = 'QF 5' + number
    elif flight['number'].startswith('DJ'):
        number = flight['number'].split(' ')[1]
        flight['code_share'] = 'VA ' + number

    primary = Flight(**flight)
    primary.save()
