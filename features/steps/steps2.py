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

@when(u'I enter "{name}" as my Twitter ID')
def impl(context, name):
    if name.startswith('@'):
        name = name[1:]
    elif name.startswith('http'):
        name = name.rsplit('/', 1)[1]
    context.twitter = name
    context.browser.form.find_control('twitter').value = name

@when(u'I enter "{email}" as my email address')
def impl(context, email):
    context.email = email
    context.browser.form.find_control('email').value = email

@when(u'I add myself with the following details')
def impl(context):
    data = dict(zip(context.table.headings, context.table.rows[0]))

    context.execute_steps(u'''
        When I select "{flight}" as my flight
        And I select "{day}" as my arrival day
        And I enter "{name}" as my name
        And I enter "{twitter}" as my Twitter ID
        And I enter "{email}" as my email address
    '''.format(**data))

@then(u'my name should link to my Twitter profile')
def impl(context):
    context.browser.response().seek(0)
    soup = BeautifulSoup(context.browser.response().read())

    name = soup.find(text=lambda t: context.name in t)
    assert name

    anchor = name.parent
    assert anchor['href'] == u'https://twitter.com/' + context.twitter

@then(u'my email address should be linked next to my name')
def impl(context):
    context.browser.response().seek(0)
    soup = BeautifulSoup(context.browser.response().read())

    name = soup.find(text=lambda t: context.name in t)
    assert name

    entry = name.find_parent('li')
    email_link = entry.find('a', text='email')
    assert email_link
    assert email_link['href'] == u'mailto:' + context.email
