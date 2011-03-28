from django.db import models
from apps.rss.models import Feed

class ContactExtra(models.Model):
    """ Abstract model to extend the RapidSMS Contact model """
    feed = models.ForeignKey(Feed)
    class Meta:
        abstract = True

  