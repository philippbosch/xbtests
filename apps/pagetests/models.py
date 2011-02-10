import re

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


class Test(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=128, blank=True)
    url = models.URLField(verbose_name=_("URL"), verify_exists=False)
    test_date = models.DateTimeField(verbose_name=_("date"))
    users = models.ManyToManyField(User, verbose_name=_("users"), blank=True)
    
    def __unicode__(self):
        return u"%s" % self.url
    
    def get_absolute_url(self):
        return reverse('test_detail', args=(self.pk,))
    
    class Meta:
        ordering = ('-test_date',)
    
    @property
    def pretty_url(self):
        return re.sub(r'^\w+\:\/\/', '', self.url)
    
    @property
    def results_count(self):
        count = 0
        for version in self.testversions.all():
            count += version.testversionresults.count()
        return count


class TestVersion(models.Model):
    test = models.ForeignKey(Test, verbose_name=_("test"), related_name="testversions")
    version_date = models.DateTimeField(verbose_name=_("date"))
    count_successful = models.PositiveIntegerField(verbose_name=_("successful results"))
    count_not_finished = models.PositiveIntegerField(verbose_name=_("not finished results"))
    version_public_url = models.URLField(verbose_name=_("public URL"), verify_exists=False)
    version_ui_url = models.URLField(verbose_name=_("user interface URL"), verify_exists=False)
    version_zip = models.URLField(verbose_name=_("zip URL"), verify_exists=False)
    w3c_css_errors = models.PositiveIntegerField(verbose_name=_("number of CSS errors"))
    w3c_html_errors = models.PositiveIntegerField(verbose_name=_("number of HTML errors"))
    w3c_html_warnings = models.PositiveIntegerField(verbose_name=_("number of HTML warnings"))
    
    def __unicode__(self):
        return u"%s @ %s" % (self.test.url, self.version_date,)
    
    class Meta:
        ordering = ('-version_date',)


class TestVersionResult(models.Model):
    testversion = models.ForeignKey(TestVersion, verbose_name=_("version"), related_name="testversionresults")
    start_date = models.DateTimeField(verbose_name=_("start date"))
    finished_date = models.DateTimeField(verbose_name=_("finished date"), blank=True, null=True)
    status = models.CharField(verbose_name=_("status"), max_length=64)
    os = models.CharField(verbose_name=_("operating system"), max_length=128)
    browser = models.CharField(verbose_name=_("browser"), max_length=128)
    resolution = models.CharField(verbose_name=_("resolution"), max_length=16)
    windowed = models.URLField(verbose_name=_("windowed screenshot URL"), verify_exists=False)
    windowed_thumb = models.URLField(verbose_name=_("windowed thumbnail URL"), verify_exists=False)
    full_page = models.URLField(verbose_name=_("full-page screenshot URL"), verify_exists=False)
    full_page_thumb = models.URLField(verbose_name=_("full-page thumb URL"), verify_exists=False)
    live_test_url = models.URLField(verbose_name=_("live test URL"), verify_exists=False)
    
    def __unicode__(self):
        return u"%s :: %s :: %s :: %s" % (self.testversion, self.os, self.browser, self.resolution)
    
    class Meta:
        ordering = ('-finished_date',)