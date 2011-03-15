__author__ = 'adewinter'
import feedparser
import re
from datetime import datetime
from models import RssStory

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
            return datetime.now()

    def create_model(self):
        story = RssStory(date_pulled=datetime.now(),
                         rss_update_date=self.get_last_update_date(),
                         story_title=self.get_title(),
                         story_contents=self.get_content())
        
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)