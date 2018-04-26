import json

from django.contrib.auth import models as auth_models
from django.test import (
    Client,
    TestCase,
)

from . import (
    models,
    utils,
)


class ListLogsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        auth_models.User.objects.create_user(
            username='thedoctor', password='rose')
        self.client.login(username='thedoctor', password='rose')

    def test_list_logs_empty(self):
        response = self.client.get('/api/v1/logs/')
        self.assertEqual(
            json.loads(response.content.decode('utf-8')), {
                'message': 'okay',
                'response': [],
                'status': 'success'
            })

    def test_list_logs(self):
        self.log = utils.slurp("""Test

        log

        file""".split('\n'), 'foo')
        response = self.client.get('/api/v1/logs/')
        self.assertEqual(
            json.loads(response.content.decode('utf-8')), {
                'message': 'okay',
                'response': [{'complete': True,
                              'date': '',
                              'id': 1,
                              'location': None,
                              'medium': '',
                              'name': 'foo',
                              'privacy': '',
                              'tags': []}],
                'status': 'success'
            })


class GetLogTestCase(TestCase):

    def setUp(self):
        self.log = utils.slurp("""Test

        log

        file""".split('\n'), 'foo')
        self.client = Client()
        auth_models.User.objects.create_user(
            username='thedoctor', password='rose')
        self.client.login(username='thedoctor', password='rose')

    def test_get_log(self):
        response = self.client.get('/api/v1/log/1/')
        self.assertEqual(
            json.loads(response.content.decode('utf-8')), {
                'message': 'okay',
                'response': {'complete': True,
                             'date': '',
                             'id': 1,
                             'lines': [{'id': 1,
                                        'line': 'Test',
                                        'moments': [],
                                        'num': 1,
                                        'participant': None,
                                        'topics': []},
                                       {'id': 2,
                                        'line': '',
                                        'moments': [],
                                        'num': 2,
                                        'participant': None,
                                        'topics': []},
                                       {'id': 3,
                                        'line': '        log',
                                        'moments': [],
                                        'num': 3,
                                        'participant': None,
                                        'topics': []},
                                       {'id': 4,
                                        'line': '',
                                        'moments': [],
                                        'num': 4,
                                        'participant': None,
                                        'topics': []},
                                       {'id': 5,
                                        'line': '        file',
                                        'moments': [],
                                        'num': 5,
                                        'participant': None,
                                        'topics': []}],
                             'location': None,
                             'medium': '',
                             'name': 'foo',
                             'privacy': '',
                             'tags': []},
                'status': 'success'})

    def test_get_log_not_found(self):
        response = self.client.get('/api/v1/log/2/')
        self.assertEqual(response.status_code, 404)
