from django.db import models


class Tag(models.Model):

    name = models.CharField(max_length=50)

    class Meta:

        abstract = True


class Location(Tag):
    pass


class ParticipantGroup(Tag):
    pass


class Moment(Tag):
    pass


class Topic(Tag):
    pass


class LogFile(models.Model):

    MEDIUM_CHOICES = (
        ('MUCK', 'MUCK'),
        ('IRC', 'IRC'),
        ('AIM', 'AOL Instant Messenger'),
        ('TGRAM', 'Telegram'),
        ('SLACK', 'Slack'),
    )
    PRIVACY_CHOICES = (
        ('public', 'Publicly visible'),
        ('private', 'Private'),
        ('back', 'Back-channel (page, whisper, etc)'),
    )

    name = models.CharField(max_length=500)
    logdate = models.DateTimeField(blank=True)
    medium = models.CharField(max_length=5, choices=MEDIUM_CHOICES)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True)
    complete = models.BooleanField(default=True)
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES)


class Participant(models.Model):

    group = models.ForeignKey(
        ParticipantGroup,
        on_delete=models.SET_NULL,
        null=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    notes = models.TextField(blank=True)


class LogLine(models.Model):

    LINE_TYPE_CHOICES = (
        ('DEF', 'Default (uncategorized)'),
        ('IM', 'Instant Message'),
        ('Meta', 'Metadata/system message'),
        ('Say', 'Say/regular message'),
        ('Pose', 'Pose/`/me` message'),
    )
    LINE_SCOPE_CHOICES = (
        ('global', 'Globally visible'),
        ('direct', 'Direct message'),
    )

    line = models.TextField()
    log_file = models.ForeignKey(LogFile, on_delete=models.CASCADE)
    participant = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True)
    line_type = models.CharField(
        max_length=4,
        choices=LINE_TYPE_CHOICES,
        default='DEF')
    line_scope = models.CharField(
        max_length=6,
        choices=LINE_SCOPE_CHOICES,
        default='global')
    moment = models.ManyToManyField(Moment)
    topic = models.ManyToManyField(Topic)