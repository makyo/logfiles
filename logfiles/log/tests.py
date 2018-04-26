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


class JoinLinesTestCase(TestCase):

    def setUp(self):
        self.log = utils.slurp("""Test

        log

        file""".split('\n'), 'foo')
        self.moment1 = models.Tag(
            name='event1',
            tag_type='m')
        self.moment1.save()
        self.moment2 = models.Tag(
            name='event2',
            tag_type='m')
        self.moment2.save()
        self.topic = models.Tag(
            name='daleks',
            tag_type='t')
        self.topic.save()
        models.LogLine.objects.get(pk=1).moments.add(self.moment1)
        models.LogLine.objects.get(pk=2).moments.add(self.moment1)
        models.LogLine.objects.get(pk=2).moments.add(self.moment2)
        models.LogLine.objects.get(pk=2).topics.add(self.topic)
        self.client = Client()
        auth_models.User.objects.create_user(
            username='thedoctor', password='rose')
        self.client.login(username='thedoctor', password='rose')

    def test_join_lines(self):
        first = models.LogLine.objects.get(pk=1)
        self.assertEqual(list(first.moments.all()), [self.moment1])
        self.assertEqual(list(first.topics.all()), [])
        response = self.client.get('/api/v1/log/1/')
        self.assertEqual(len(response.json()['response']['lines']), 5)
        response = self.client.post('/api/v1/log/1/join-lines/', {
            'lines': ['1', '2', '3'],
        })
        self.assertEqual(
            response.json()['response']['line'], 'Test\n\n        log')
        response = self.client.get('/api/v1/log/1/')
        self.assertEqual(len(response.json()['response']['lines']), 3)
        first = models.LogLine.objects.get(pk=1)
        self.assertEqual(
            list(first.moments.all()), [self.moment1, self.moment2])
        self.assertEqual(list(first.topics.all()), [self.topic])


class SetLineTypeTestCase(TestCase):

    def setUp(self):
        self.log = utils.slurp("""Test

        log

        file""".split('\n'), 'foo')
        self.client = Client()
        auth_models.User.objects.create_user(
            username='thedoctor', password='rose')
        self.client.login(username='thedoctor', password='rose')

    def test_set_type(self):
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.line_type, '_DEF')
        self.client.post('/api/v1/line/1/set/', {
            'type': 'type',
            'value': 'Meta',
        })
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.line_type, 'Meta')

    def test_set_scope(self):
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.line_scope, 'global')
        self.client.post('/api/v1/line/1/set/', {
            'type': 'scope',
            'value': 'direct',
        })
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.line_scope, 'direct')


class LineTagTestCase(TestCase):

    def setUp(self):
        self.log = utils.slurp("""Test

        log

        file""".split('\n'), 'foo')
        self.moment = models.Tag(
            name='event',
            tag_type='m')
        self.moment.save()
        self.topic = models.Tag(
            name='daleks',
            tag_type='t')
        self.topic.save()
        self.client = Client()
        auth_models.User.objects.create_user(
            username='thedoctor', password='rose')
        self.client.login(username='thedoctor', password='rose')

    def test_add_remove_moment(self):
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.moments.count(), 0)
        self.client.post('/api/v1/line/1/tag/add/', {
            'type': 'moment',
            'value': self.moment.id,
        })
        self.assertEqual(line.moments.count(), 1)
        self.assertEqual(line.moments.all()[0], self.moment)
        self.client.post('/api/v1/line/1/tag/remove/', {
            'type': 'moment',
            'value': self.moment.id,
        })
        self.assertEqual(line.moments.count(), 0)

    def test_add_remove_topic(self):
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.topics.count(), 0)
        self.client.post('/api/v1/line/1/tag/add/', {
            'type': 'topic',
            'value': self.topic.id,
        })
        self.assertEqual(line.topics.count(), 1)
        self.assertEqual(line.topics.all()[0], self.topic)
        self.client.post('/api/v1/line/1/tag/remove/', {
            'type': 'topic',
            'value': self.topic.id,
        })
        self.assertEqual(line.topics.count(), 0)

    def test_add_unlike_types_failure(self):
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.topics.count(), 0)
        response = self.client.post('/api/v1/line/1/tag/add/', {
            'type': 'topic',
            'value': self.moment.id,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['message'],
            'Invalid tag type, expected topic, got moment')

    def test_remove_nonexistant_tag_failure(self):
        line = models.LogLine.objects.get(pk=1)
        self.assertEqual(line.topics.count(), 0)
        response = self.client.post('/api/v1/line/1/tag/remove/', {
            'type': 'topic',
            'value': self.topic.id,
        })
        self.assertEqual(response.json()['message'], 'topic not found in line')
        self.assertEqual(line.topics.count(), 0)
