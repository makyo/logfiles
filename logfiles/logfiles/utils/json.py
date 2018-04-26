import json

from django.http import HttpResponse


def success(response):
    content = json.dumps({
        'status': 'success',
        'message': 'okay',
        'response': response,
    })
    return HttpResponse(content, content_type='application/json')


def error(code, message, response=None):
    content_obj = {
        'status': 'error',
        'message': message,
    }
    if response is not None:
        content_obj['response'] = response
    content = json.dumps(content_obj)
    return HttpResponse(
        content,
        status=code,
        content_type='application/json')
