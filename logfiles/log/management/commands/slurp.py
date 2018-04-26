import argparse
import hashlib

from django.core.management.base import BaseCommand, CommandError

from log import models


class Command(BaseCommand):
    help = 'Slurps a file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            nargs=1,
            type=argparse.FileType('r'))

    def handle(self, *args, **options):
        contents = []
        for line in options['file'][0]:
            contents.append(line)
        contents_hash = hashlib.sha256('\n'.join(contents).encode()).hexdigest()
        if models.LogFile.objects.filter(contents_hash=contents_hash).count():
            raise CommandError('that log appears to already be in the DB!'
                               ' sha256 = {}'.format(contents_hash))
        logfile = models.LogFile(
            name=options['file'][0].name,
            contents_hash=contents_hash)
        logfile.save()
        for line in enumerate(contents):
            logline = models.LogLine(
                line=line[1],
                line_num=line[0] + 1,
                log_file = logfile)
            logline.save()
