from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.messages.outgoing import OutgoingMessage
from rapidsms.models import Contact
import logging

SUCCESS_MSG = "RSS Stories sent out to demo participants!"
logger = logging.getLogger('rss.handlers.demo')
class TriggerHandler(KeywordHandler):
    keyword = "trigger|TRIGGER"

    def handle(self, text):
        self.respond("Read Trigger kw with args: %s" % text)


    def help(self):
        self.fire_ze_missiles()


    def fire_ze_missiles(self):
        contacts_with_feeds = Contact.objects.filter(feed__isnull=False)
        #assumes contacts are correctly set up with an identity etc.
        for contact in contacts_with_feeds:
            if contact.default_connection is None:
                logging.warn("Can't send to %s as they have no connections" % contact)
                continue
            story_txt = '%s::%s' % (contact.feed.get_latest_story().story_title, contact.feed.get_latest_story().story_contents)
            print 'Contact default backend=%s' % contact.default_connection
            OutgoingMessage(contact.default_connection, story_txt).send()

        self.respond(SUCCESS_MSG)
