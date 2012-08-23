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
