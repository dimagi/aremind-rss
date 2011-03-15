from django.core.exceptions import ObjectDoesNotExist

__author__ = 'adewinter'
import feedparser
import re
import logging
from datetime import datetime
from models import RssStory, Feed

logger = logging.getLogger('rss.models')

class Feed():
    feed_url = ""
    feed = None

    ''' Used to indicate if there was a problem parsing the feed '''
    broken = False
    broken_msg = ''


    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.feed = feedparser.parse(feed_url)

    def get_title(self):
        '''
        Returns the latest entry title
        '''
        try:
            return self.feed.entries[0].title
        except AttributeError:
            self.broken = True
            self.broken_msg = "Problem parsing latest entry title!"
            return ""

    def get_content(self, limit=False):
        '''
        Returns the content (stripped of html).
        If limit is set to True, the returned String
        will be limited to 140 Chars (to allow for 20 chars
        of additional information to be added to a standard
        length (160 char) message.
        '''
        try:
            body = self.feed.entries[0].summary
            body = remote_html_tags(body)
            if limit:
                return body[:140]
            else:
                return body
        except AttributeError:
            self.broken = True
            self.broken_msg = "Problem parsing latest entry content!"
            return ""


    def get_last_update_date(self):
        '''
        Gets the last datetime when this module was updated.
        '''
        try:
            d = self.feed.entries[0].updated_parsed
            return datetime(*d[:6])
        except AttributeError:
            self.broken = True
            self.broken_msg = "Problem parsing feed updated_date. Defaulting to now()."
            logger.debug("%s URL: %s" % (self.broken_msg, self.feed_url))
            return datetime.now()

    def create_model(self):
        try:
            related_feed_model = Feed.objects.get(feed_url=self.feed_url)
        except:
            logger.warn('Could not find a Feed model to associate with this story! Cannot create RssStory For feed_url: %s' % self.feed_url)

        story = RssStory(date_pulled=datetime.now(),
                         rss_update_date=self.get_last_update_date(),
                         story_title=self.get_title(),
                         story_contents=self.get_content(),
                         feed=related_feed_model)
        
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def update_stories(feed_models):
    for feed in feed_models:
        new_story = Feed(feed.feed_url).create_model()
        try:
            old_story = RssStory.objects.get(rss_update_date=new_story.rss_update_date, feed=new_story.feed)
            new_story.delete() #we don't need to save dupes.
        except ObjectDoesNotExist:
            new_story.save()
            continue
    return
