from datetime import datetime

__author__ = 'adewinter'
from django.db import models

class RssStory(models.Model):
    date_pulled = models.DateTimeField(default=datetime.now, blank=False,null=False)
    rss_update_date = models.DateTimeField()
    story_title = models.CharField(max_length=255)
    story_contents = models.TextField(null=False,blank=False)

