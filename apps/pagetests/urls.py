from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from .views import TestListView, TestDetailView


urlpatterns = patterns('', 
    url(r'^$', login_required(TestListView.as_view()), name="test_list"),
    url(r'^(?P<pk>\d+)/$', login_required(TestDetailView.as_view()), name="test_detail"),
)
