import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import (
    LogFile,
    LogLine,
    Participant,
    Tag,
)
from logfiles.utils.json import (
    error,
    success,
)


@require_http_methods(['GET'])
@login_required
def list_logs(request):
    """List all logs."""
    return success([log.to_object() for log in LogFile.objects.all()])


@require_http_methods(['GET'])
@login_required
def get_log(request, log_id):
    """Retrieve a single log."""
    log = get_object_or_404(LogFile, pk=int(log_id))
    return success(log.to_object(lines=True))


@require_http_methods(['GET'])
@login_required
def join_lines(request):
    """Join multiple lines together into one."""
    payload = json.loads(request.body.decode('utf-8'))
    lines = [Line.objects.get(pk=line) for line in sorted(payload.lines)]
    first = lines[0]
    lines = lines[1:]
    for line in lines:
        first.line += ' {}'.format(line.line)
        for moment in line.moments.all():
            if moment not in first.moments:
                first.moments.append(moment)
        for topic in line.topics.all():
            if topic not in first.topics.all():
                first.topics.append(topic)
        line.delete()
    first.save()
    return success(first.to_object())


@require_http_methods(['POST'])
@login_required
def set_line_type(request, line_id):
    """Set the line type or scope."""
    payload = json.loads(request.body.decode('utf-8'))
    line = Line.objects.get(pk=line_id)
    if 'type' in payload:
        line.line_type = payload.get('type')
    elif 'scope' in payload:
        line.line_scope = request.GET.get('scope')
    return success(None)


@require_http_methods(['POST'])
@login_required
def add_line_tag(request, line_id):
    """Add a tag (participant, moment, topic) to a line."""
    payload = json.loads(request.body.decode('utf-8'))
    line = Line.objects.get(pk=line_id)
    pass


@require_http_methods(['POST'])
@login_required
def remove_line_tag(request, line_id):
    """Remove a tag (participant, moment, topic) from a line."""
    payload = json.loads(request.body.decode('utf-8'))
    line = Line.objects.get(pk=line_id)
    pass
