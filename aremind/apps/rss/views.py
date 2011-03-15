from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response

from models import FeedForm, Feed, RssStory

def edit_feed(request, feed_id):
    '''
    View used for editing and manually updating feeds
    '''
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            f = Feed.objects.get(pk=feed_id)
            feed = FeedForm(request.post, instance=f)
            feed.save()
            return HttpResponseRedirect('/show_feeds/') # Redirect after POST

    try:
        form = FeedForm(instance=Feed.objects.get(pk=feed_id))
    except ObjectDoesNotExist:
        form = FeedForm()

    context = {'form': form}
    return render_to_response('rss/edit_feed.html', {}, RequestContext(request))

def new_feed(request, feed_id):
    '''
    Create a new feed
    '''
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/thanks/') # Redirect after POST
        else:
            form = FeedForm() # An unbound form

    form = FeedForm()
    context = {'form': form}
    return render_to_response('rss/new_feed.html', context, RequestContext(request))

def show_current_stories(request):
    '''
    A quick overview of the current story from each feed
    '''
    stories = RssStory.objects.all()
    context = {'stories': stories}
    return render_to_response('rss/current_stories.html', context, RequestContext(request))

def show_feeds(request):
    '''
    Show existing feeds (with 'edit' button for each feed)
    '''
    feeds = Feed.objects.all()
    context = {'feeds': feeds}
    return render_to_response('rss/show_feeds.html', context, RequestContext(request))
    

def dashboard(request):
    '''
    Default dashboard view for RSS app
    '''
    return render_to_response('rss/dashboard.html', {}, RequestContext(request))


