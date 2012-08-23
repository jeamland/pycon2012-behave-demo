from bs4 import BeautifulSoup, Tag
import mechanize

from behave import *

@given(u'I am at the PyCon AU meetup page')
def impl(context):
    context.browser.open(context.browser_url('/'))
    context.browser.select_form(nr=0)

@when(u'I select "{flight}" as my flight')
def impl(context, flight):
    context.flight = flight

    control = context.browser.form.find_control('flight')
    items = control.get_items()
    for item in control.get_items():
        if flight in item.attrs['label']:
            control.value = [item.attrs['value']]
            return

    assert False

@when(u'I select "{day}" as my arrival day')
def impl(context, day):
    context.day = day.lower().title()

    control = context.browser.form.find_control('day')
    items = control.get_items()
    for item in control.get_items():
        if item.attrs['label'].lower() == day.lower():
            control.value = [item.attrs['value']]
            return

    assert False

@when(u'I enter "{name}" as my name')
def impl(context, name):
    context.name = name
    context.browser.form.find_control('name').value = name

@when(u'I click "Add me!"')
def impl(context):
    context.browser.submit()

@then(u'my flight should appear in the flights table')
def impl(context):
    context.browser.response().seek(0)
    soup = BeautifulSoup(context.browser.response().read())

    table = soup.find('table')
    flight_row = table.find('td', text=lambda t: context.flight in t).parent
    assert flight_row is not None

    for row in flight_row.previous_siblings:
        if type(row) is not Tag:
            continue
        if row.find('td', text=context.day):
            return
        elif row.find('td', colspan='6'):
            break
    assert False

@then(u'my name should appear next to my flight')
def impl(context):
    context.browser.response().seek(0)
    soup = BeautifulSoup(context.browser.response().read())

    name = soup.find(text=lambda t: context.name in t)
    assert name
    row = name.find_parent('tr')
    assert row.find(text=lambda t: context.flight in t)
