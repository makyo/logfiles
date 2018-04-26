import argparse
import hashlib

from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic

from log import utils


class Command(BaseCommand):
    help = 'Slurps a file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            nargs=1,
            type=argparse.FileType('r'))

    @atomic
    def handle(self, *args, **options):
        contents = []
        for line in options['file'][0]:
            contents.append(line)
        try:
            utils.slurp(contents, options['file'][0].name)
        except Exception as e:
            raise CommandError(e)
