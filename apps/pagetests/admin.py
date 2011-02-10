from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Test, TestVersion, TestVersionResult


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'test_date',)
    readonly_fields = ('url', 'test_date',)

admin.site.register(Test, TestAdmin)


class TestVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'version_date', 'stats')
    list_filter = ('test',)
    readonly_fields = ('test', 'version_date', 'count_successful', 'count_not_finished', 'version_public_url', 'version_ui_url', 'version_zip', 'w3c_html_errors', 'w3c_html_warnings', 'w3c_css_errors',)
    
    def stats(self, instance):
        return u"%s/%s" % (instance.count_successful, instance.count_not_finished)

admin.site.register(TestVersion, TestVersionAdmin)


class TestVersionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'version_date', 'os', 'browser', 'resolution', 'thumb_tag',)
    list_filter = ('testversion', 'os', 'browser', 'resolution',)
    readonly_fields = ('testversion', 'start_date', 'finished_date', 'status', 'os', 'browser', 'resolution', 'windowed_thumb', 'windowed', 'full_page_thumb', 'full_page', 'live_test_url',)
    list_per_page = 10
    
    def url(self, instance):
        return instance.testversion.test.url
    
    def version_date(self, instance):
        return instance.testversion.version_date
    
    def thumb_tag(self, instance):
        return '<img src="%s">' % instance.windowed_thumb
    thumb_tag.short_description = _("thumbnail")
    thumb_tag.allow_tags = True

admin.site.register(TestVersionResult, TestVersionResultAdmin)
