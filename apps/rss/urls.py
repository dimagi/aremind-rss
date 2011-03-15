from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^', views.dashboard),
    url(r'^editfeeds/$', views.edit_feeds, name='edit-feeds'),
    url(r'^showfeeds/$', views.show_current_stories, name='show-feeds')
)