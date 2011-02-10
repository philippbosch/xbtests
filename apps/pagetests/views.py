from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Test


class TestMixin(object):
    model = Test
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return Test.objects.filter(users=self.request.user)


class TestListView(TestMixin, ListView):
    context_object_name = 'test_list'


class TestDetailView(TestMixin, DetailView):
    context_object_name = 'test'
