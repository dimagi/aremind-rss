# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Feed'
        db.create_table('rss_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('feed_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('rss', ['Feed'])

        # Adding model 'RssStory'
        db.create_table('rss_rssstory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_pulled', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('rss_update_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('story_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('story_contents', self.gf('django.db.models.fields.TextField')()),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='current_story', to=orm['rss.Feed'])),
        ))
        db.send_create_signal('rss', ['RssStory'])


    def backwards(self, orm):
        
        # Deleting model 'Feed'
        db.delete_table('rss_feed')

        # Deleting model 'RssStory'
        db.delete_table('rss_rssstory')


    models = {
        'rss.feed': {
            'Meta': {'object_name': 'Feed'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'feed_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'rss.rssstory': {
            'Meta': {'object_name': 'RssStory'},
            'date_pulled': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'current_story'", 'to': "orm['rss.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rss_update_date': ('django.db.models.fields.DateTimeField', [], {}),
            'story_contents': ('django.db.models.fields.TextField', [], {}),
            'story_title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['rss']
