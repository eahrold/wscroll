from django.conf.urls import patterns, url
from wscroll import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^page/add/$', views.page_add,{}, name='page_add'),    
    url(r'^page/delete/(?P<id>\d+)/$', views.page_delete, name='page_delete'),
    
    url(r'^collection/add/$', views.collection_add, name='collection_add'),
    url(r'^collection/add_index/$', views.collection_add_from_index, name='collection_add_from_index'), 
    
    url(r'^collection/edit/(?P<collection_id>\d+)/$', views.collection_edit, name='collection_edit'),
    url(r'^collection/delete/(?P<id>\d+)/$', views.collection_delete, name='collection_delete'),
    url(r'^collection/details/(?P<id>\d+)/$', views.collection_details, name='collection_details'), 

    url(r'^(?P<name>[^/]+)/$', views.getlist, name='getlist'),
)