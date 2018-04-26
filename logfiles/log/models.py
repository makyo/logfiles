from django.db import models


class Tag(models.Model):
    """Tag holds an arbitrary tag string to attach to another model."""

    TAG_TYPE_CHOICES = (
        ('u', 'tag'),
        ('l', 'location'),
        ('p', 'participant group'),
        ('m', 'moment'),
        ('t', 'topic')
    )

    name = models.CharField(max_length=50)
    tag_type = models.CharField(
        max_length=1,
        choices=TAG_TYPE_CHOICES,
        default='t')

    def to_object(self, related=False):
        """Return a dict representation of the model with optional related
        fields.
        """
        obj = {
            'id': self.id,
            'tag': self.name,
            'type': self.get_tag_type_display(),
        }
        if related:
            if self.tag_type == 'l':
                obj['related'] = [
                    log.to_object() for logs in self.location_logs.all()]
            elif self.type == 'p':
                obj['related'] = [
                    participant.to_object(alts=False) for participant in
                    self.alt_group.all()]
            elif self.type == 'm':
                obj['related'] = [
                    line.to_object() for line in self.line_moments.all()]
            elif self.type == 't':
                obj['related'] = [
                    line.to_object() for line in self.line_topics.all()]
            elif self.type == 'u':
                obj['related'] = [
                    log.to_object() for logs in self.logs.all()]
        return obj


class LogFile(models.Model):
    """LogFile represents a single file and all its contents and metadata."""

    MEDIUM_CHOICES = (
        ('muck', 'MUCK'),
        ('irc', 'IRC'),
        ('aim', 'AOL Instant Messenger'),
        ('tgram', 'Telegram'),
        ('slack', 'Slack'),
    )
    PRIVACY_CHOICES = (
        ('public', 'Publicly visible'),
        ('private', 'Private'),
        ('back', 'Back-channel (page, whisper, etc)'),
    )

    name = models.CharField(max_length=500)
    contents_hash = models.CharField(max_length=100)
    log_date = models.DateTimeField(null=True)
    medium = models.CharField(max_length=5, choices=MEDIUM_CHOICES, blank=True)
    complete = models.BooleanField(default=True)
    privacy = models.CharField(
        max_length=7,
        choices=PRIVACY_CHOICES,
        blank=True)
    location = models.ForeignKey(
        Tag,
        related_name='location_logs',
        on_delete=models.SET_NULL,
        null=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='logs')

    def to_object(self, lines=False):
        """Return a dict representation of the model with optional related
        fields.
        """
        obj = {
            'id': self.id,
            'name': self.name,
            'date': self.log_date.isoformat(' ') if self.log_date else '',
            'medium': self.get_medium_display(),
            'complete': self.complete,
            'privacy': self.get_privacy_display(),
            'location': self.location.to_object() if self.location else None,
            'tags': [tag.to_object() for tag in self.tags.all()],
        }
        if lines:
            obj['lines'] = [
                line.to_object(log=False) for line in self.logline_set.all()]
        return obj


class Participant(models.Model):
    """Participant represents the one who sent a line."""

    group = models.ForeignKey(
        Tag,
        related_name='alt_group',
        on_delete=models.SET_NULL,
        null=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def to_object(self, alts=True):
        """Return a dict representation of the model with optional related
        fields.
        """
        obj = {
            'name': self.name,
            'gender': self.gender,
            'notes': self.notes,
        }
        if alts:
            obj['alts'] = []
            if self.group:
                obj['alts'] = [
                    alt.to_object(alts=False) for alt in
                    self.group.participant_set.all()]
        return obj


class LogLine(models.Model):
    """LogLine holds a single line of a log and its metadata."""

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
    line_num = models.IntegerField()
    log_file = models.ForeignKey(LogFile, on_delete=models.CASCADE)
    participant = models.ForeignKey(
        Tag,
        related_name="line_participants",
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
    moments = models.ManyToManyField(
        Tag,
        related_name='line_moments')
    topics = models.ManyToManyField(
        Tag,
        related_name='line_topics')

    class Meta:
        ordering = ['line_num']

    def to_object(self, log=True):
        """Return a dict representation of the model with optional related
        fields.
        """
        obj = {
            'id': self.id,
            'line': self.line,
            'num': self.line_num,
            'participant':
                self.participant.to_object() if self.participant else None,
            'moments': [moment.to_object() for moment in self.moments.all()],
            'topics': [topic.to_object() for topic in self.topics.all()],
        }
        if log:
            obj['log'] = self.log_file.to_object()
        return obj
