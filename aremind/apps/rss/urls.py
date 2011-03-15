from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^', views.dashboard),
    url(r'^feeds/$', views.show_feeds),
    url(r'^editfeed/(?P<feed_id>\d+)/$', views.edit_feed),
    url(r'^newfeed/(?P<feed_id>\d+)/$', views.new_feed),
    url(r'^stories/$', views.show_current_stories),
    url(r'^dashboard/$', views.dashboard),
)