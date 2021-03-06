from datetime import datetime
from django.forms.models import ModelForm

__author__ = 'adewinter'
from django.db import models

class Feed(models.Model):
    date_added = models.DateTimeField(default=datetime.now, blank=False, null=False)
    feed_url = models.CharField(max_length=255, blank=False, null=False,help_text ="The RSS Feed URL")
    description = models.CharField(max_length=255, help_text="A Brief description of the RSS Feed")

    def __unicode__(self):
        return '%s :: %s' % (self.description, self.feed_url)


    def get_latest_story(self):
        return self.current_story.latest(field_name='date_pulled')

class FeedForm(ModelForm):
    class Meta:
        model = Feed

class RssStory(models.Model):
    date_pulled = models.DateTimeField(default=datetime.now, blank=False,null=False)
    rss_update_date = models.DateTimeField()
    story_title = models.CharField(max_length=255)
    story_contents = models.TextField(null=False,blank=False)
    feed = models.ForeignKey(Feed, null=False, blank=False, related_name='current_story')

    def __unicode__(self):
        return '%s: %s' % (self.story_title, self.story_contents)