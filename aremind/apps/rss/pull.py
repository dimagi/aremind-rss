from django.core.exceptions import ObjectDoesNotExist

__author__ = 'adewinter'
import feedparser
import re
import logging
from datetime import datetime
from models import RssStory, Feed

logger = logging.getLogger('rss.models')


def get_title(parsed_feed):
    '''
    Returns the latest entry title
    '''
    try:
        if len(parsed_feed.feed) == 0:
            raise AttributeError

        return parsed_feed.entries[0].title
    except AttributeError:
        logger.error("Problem parsing latest entry title!")
        raise AttributeError

def get_content(parsed_feed, limit=None):
    '''
    Returns the content (stripped of html).
    If limit is set to True, the returned String
    will be limited to 140 Chars (to allow for 20 chars
    of additional information to be added to a standard
    length (160 char) message.
    '''
    try:
        if len(parsed_feed.feed) == 0:
            raise AttributeError

        body = parsed_feed.entries[0].summary
        body = remove_html_tags(body)
        if limit:
            return body[:limit]
        else:
            return body
    except AttributeError:
        logger.error("Problem parsing latest entry content!")
        raise AttributeError


def get_last_update_date(parsed_feed):
    '''
    Gets the last datetime when this module was updated.
    '''
    try:
        d = parsed_feed.entries[0].updated_parsed
        return datetime(*d[:6])
    except AttributeError:
        logger.error("Problem parsing feed updated_date. Defaulting to now().")
        return datetime.now()

def generate_new_story(feed):
    '''
    Grabs the latest story from the feed_url specified
    in feed. Automatically creates a new RssStory Model
    and saves it.
    '''
    parsed_feed = feedparser.parse(feed.feed_url)
    if len(parsed_feed.feed) == 0:
            logger.error("Unable to generate new story for feed at URL %s" % feed.feed_url)
            raise AttributeError


    try:
        story = RssStory(date_pulled=datetime.now(),
                         rss_update_date=get_last_update_date(parsed_feed),
                         story_title=get_title(parsed_feed),
                         story_contents=get_content(parsed_feed),
                         feed=feed)
        story.save()
    except AttributeError:
        logger.error("Unable to generate new story for feed at URL %s" % feed.feed_url)

def remove_html_tags(data):
    '''
    A very quick and dirty html stripper.
    Aim: remove html junk to get as much plaintext from the feed as possible.
    '''
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def update_stories(feed_models):
    for feed in feed_models:
        generate_new_story(feed)
