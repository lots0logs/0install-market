from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

class App(models.Model):
    NETWORK = 'NWK'
    AUDIO_VIDEO = 'A_V'
    GRAPHICS = 'IMG'
    OFFICE = 'OFF'
    SYSTEM = 'SYS'
    EDUCATION = 'EDU'
    GAME = 'GAM'
    UTILITIES = 'UTI'
    SETTINGS = 'SET'
    DEVELOPMENT = 'DEV'
    SCIENCE = 'SCI'
    CATEGORY_OPTIONS = (
        (NETWORK,     'Network'),
        (AUDIO_VIDEO, 'AudioVideo'),
        (GRAPHICS,    'Graphics'),
        (OFFICE,      'Office'),
        (SYSTEM,      'System'),
        (EDUCATION,   'Education'),
        (GAME,        'Game'),
        (UTILITIES,   'Utilities'),
        (SETTINGS,    'Settings'),
        (DEVELOPMENT, 'Development'),
        (SCIENCE,     'Science'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    xml = models.URLField(null=False, unique=True)
    homepage = models.URLField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated_date = models.DateTimeField('date updated', auto_now=True)
    uploader = models.ForeignKey(User)
    category = models.CharField(max_length=3,
                                choices=CATEGORY_OPTIONS)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('market.apps.views.app', args=[str(self.pk)])

class Review(models.Model):
    RATING_OPTIONS = [(i,i) for i in range(1,6)]
    rating = models.IntegerField(choices=RATING_OPTIONS)
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User)
    app = models.ForeignKey(App)
