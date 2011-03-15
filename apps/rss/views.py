__author__ = 'adewinter'
from django.shortcuts import render_to_response

def edit_feeds(request):
    '''
    View used for editing and manually updating feeds
    '''
    return render_to_response(request)

def show_current_stories(request):
    '''
    A quick overview of the current story from each feed
    '''

def dashboard(request):
    '''
    Default dashboard view for RSS app
    '''
    return render_to_response(request)

