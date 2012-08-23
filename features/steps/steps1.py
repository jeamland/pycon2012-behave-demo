from bs4 import BeautifulSoup
import requests

from behave import *

@when(u'I fetch the meetup page')
def impl(context):
    context.page = requests.get(context.browser_url('/')).content

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
