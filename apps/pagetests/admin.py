from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Test, TestVersion, TestVersionResult


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'test_date')

admin.site.register(Test, TestAdmin)


class TestVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'version_date', 'stats')
    list_filter = ('test',)
    
    def stats(self, instance):
        return u"%s/%s" % (instance.count_successful, instance.count_not_finished)

admin.site.register(TestVersion, TestVersionAdmin)


class TestVersionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'version_date', 'os', 'browser', 'resolution', 'thumb_tag',)
    list_filter = ('testversion', 'os', 'browser', 'resolution',)
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
