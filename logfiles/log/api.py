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


@require_http_methods(['POST'])
@login_required
def join_lines(request, log_id):
    """Join multiple lines together into one."""
    to_join = [int(line) for line in request.POST.getlist('lines')]
    lines = [
        get_object_or_404(
            LogLine, pk=line, log_file__id=log_id)
        for line in sorted(to_join)]
    first = lines[0]
    lines = lines[1:]
    for line in lines:
        first.line += '\n{}'.format(line.line)
        for moment in line.moments.all():
            if moment not in first.moments.all():
                first.moments.add(moment)
        for topic in line.topics.all():
            if topic not in first.topics.all():
                first.topics.add(topic)
        line.delete()
    first.save()
    return success(first.to_object())


@require_http_methods(['POST'])
@login_required
def set_line_type(request, line_id):
    """Set the line type or scope."""
    line = get_object_or_404(LogLine, pk=line_id)
    if request.POST.get('type') == 'type':
        line.line_type = request.POST.get('value')
    elif request.POST.get('type') == 'scope':
        line.line_scope = request.POST.get('value')
    line.save()
    return success(line.to_object())


@require_http_methods(['POST'])
@login_required
def add_line_tag(request, line_id):
    """Add or remove a tag (moment, topic) to a line."""
    line = get_object_or_404(LogLine, pk=line_id)
    tag = get_object_or_404(Tag, pk=request.POST.get('value'))
    if request.POST.get('type') == 'moment':
        if tag.tag_type != 'm':
            return error(400,
                'Invalid tag type, expected moment, got {}'.format(
                    tag.get_tag_type_display()))
        line.moments.add(tag)
    elif request.POST.get('type') == 'topic':
        if tag.tag_type != 't':
            return error(400, 'Invalid tag type, expected topic, got {}'.format(
                tag.get_tag_type_display()))
        line.topics.add(tag)
    line.save()
    return success(line.to_object())


@require_http_methods(['POST'])
@login_required
def remove_line_tag(request, line_id):
    """Add or remove a tag (moment, topic) to a line."""
    line = get_object_or_404(LogLine, pk=line_id)
    tag = get_object_or_404(Tag, pk=request.POST.get('value'))
    if request.POST.get('type') == 'moment':
        if tag not in line.moments.all():
            return error(404, 'moment not found in line')
        line.moments.remove(tag)
    elif request.POST.get('type') == 'topic':
        if tag not in line.topics.all():
            return error(404, 'topic not found in line')
        line.topics.remove(tag)
    line.save()
    return success(line.to_object())
