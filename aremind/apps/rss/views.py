from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.contrib import messages

from models import FeedForm, Feed, RssStory
import pull
from django.core.urlresolvers import reverse

def edit_feed(request, feed_id):
    '''
    View used for editing and manually updating feeds
    '''
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            f = Feed.objects.get(pk=feed_id)
            feed = FeedForm(request.POST, instance=f)
            feed.save()
            return HttpResponseRedirect(reverse(show_feeds)) # Redirect after POST

    try:
        form = FeedForm(instance=Feed.objects.get(pk=feed_id))
    except ObjectDoesNotExist:
        form = FeedForm()

    context = {'form': form}
    return render_to_response('rss/edit_feed.html', context, RequestContext(request))

def new_feed(request):
    '''
    Create a new feed
    '''
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect(reverse(show_feeds)) # Redirect after POST
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
    context = {}
    if request.method == 'POST':
        if request.POST['update']:
            pull.update_stories()

    if request.GET.__contains__('delete_id'):

        try:
            f = Feed.objects.get(pk=request.GET['delete_id'])
            f.delete()
            messages.info(request,'Feed deleted succesfully!')
        except ObjectDoesNotExist:
            messages.error(request,'Could not find an object with that ID! Nothing to delete.')

    feeds = Feed.objects.all()
    context['feeds']= feeds
    return render_to_response('rss/show_feeds.html', context, RequestContext(request))
    

def dashboard(request):
    '''
    Default dashboard view for RSS app
    '''
    return render_to_response('rss/dashboard.html', {}, RequestContext(request))


