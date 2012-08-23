from bs4 import BeautifulSoup
import requests

from behave import *

SERVER_URL = 'http://127.0.0.1:8000/'

@when(u'I fetch the meetup page')
def impl(context):
    context.page = requests.get(SERVER_URL).content
