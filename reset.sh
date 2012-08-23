#!/bin/sh

rm meetup.db
python manage.py syncdb --noinput
python manage.py loaddata flights.json
