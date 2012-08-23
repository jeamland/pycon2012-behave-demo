from bs4 import BeautifulSoup
import requests

from behave import *

SERVER_URL = 'http://127.0.0.1:8000/'

@when(u'I fetch the meetup page')
def impl(context):
    context.page = requests.get(SERVER_URL).content

@then(u'I should see the meetup form')
def impl(context):
    soup = BeautifulSoup(context.page)
    form = soup.find('form')
    assert form is not None
    assert form['action'] == '/add'

@then(u'I should see the flights table')
def impl(context):
    soup = BeautifulSoup(context.page)
    table = soup.find('table')
    assert table is not None
    assert len(list(table.find_all('tr'))) > 0
