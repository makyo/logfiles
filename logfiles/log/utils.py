import hashlib

from . import models


def slurp(contents, name):
    contents_hash = hashlib.sha256('\n'.join(contents).encode()).hexdigest()
    if models.LogFile.objects.filter(contents_hash=contents_hash).count():
        raise KeyError('that log appears to already be in the DB!'
                           ' sha256 = {}'.format(contents_hash))
    logfile = models.LogFile(
        name=name,
        contents_hash=contents_hash)
    logfile.save()
    for line in enumerate(contents):
        logline = models.LogLine(
            line=line[1],
            line_num=line[0] + 1,
            log_file = logfile)
        logline.save()
    return logfile
