import os
import urlparse

from django.core.handlers.wsgi import WSGIHandler
from django.core import management

from wsgi_intercept import add_wsgi_intercept, httplib_intercept, \
                           mechanize_intercept, wsgi_fake_socket

from pycon import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'pycon.settings'

wsgi_fake_socket.settimeout = lambda x, y: None
httplib_intercept.install()

def before_all(context):
    management.setup_environ(settings)

    from django.test.simple import DjangoTestSuiteRunner
    context.runner = DjangoTestSuiteRunner()

    host = context.host = 'localhost'
    port = context.port = 8765

    add_wsgi_intercept(host, port, WSGIHandler)

    def browser_url(url):
        return urlparse.urljoin('http://%s:%d/' % (host, port), url)

    context.browser_url = browser_url

def before_scenario(context, scenario):
    context.runner.setup_test_environment()
    context.old_db_config = context.runner.setup_databases()

    management.call_command('loaddata', 'flights.json')

    browser = context.browser = mechanize_intercept.Browser()
    browser.set_handle_robots(False)

def after_scenario(context, scenario):
    context.runner.teardown_databases(context.old_db_config)
    context.runner.teardown_test_environment()
