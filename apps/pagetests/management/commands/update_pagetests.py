from django.conf import settings
from django.core.management.base import NoArgsCommand

from xbtesting import XBTesting

from ...models import Test, TestVersion, TestVersionResult


class Command(NoArgsCommand):
    help = 'Update the database with fresh data from CrossBrowserTesting.com'
    
    def handle_noargs(self, **options):
        XBTesting.username = getattr(settings, 'XBTESTING_USERNAME')
        XBTesting.password = getattr(settings, 'XBTESTING_PASSWORD')
        xbt = XBTesting()
        
        # Tests
        xbtests = xbt.get_tests()
        for xbtest in xbtests:
            self.stdout.write("Test #%s\n" % xbtest.id)
            test_attr_keys = ('id', 'url', 'test_date',)
            try:
                test = Test.objects.get(id=xbtest.id)
                for key in test_attr_keys:
                    setattr(test, key, getattr(xbtest, key))
                test.save()
            except Test.DoesNotExist:
                test = Test.objects.create(**dict([(key, getattr(xbtest, key)) for key in test_attr_keys]))
            
            # TestVersions
            xbtestversions = xbtest.get_versions()
            for xbtestversion in xbtestversions:
                self.stdout.write("TestVersion #%s\n" % xbtestversion.id)
                testversion_attr_keys = ('id', 'version_date', 'count_successful', 'count_not_finished', 'version_public_url', 'version_ui_url', 'version_zip', 'w3c_css_errors', 'w3c_html_errors', 'w3c_html_warnings')
                try:
                    testversion = TestVersion.objects.get(id=xbtestversion.id)
                    for key in testversion_attr_keys:
                        setattr(testversion, key, getattr(xbtestversion, key))
                        testversion.test = test
                    testversion.save()
                except TestVersion.DoesNotExist:
                    testversion_attrs = dict([(key, getattr(xbtestversion, key)) for key in testversion_attr_keys])
                    testversion_attrs.update(test=test)
                    testversion = TestVersion.objects.create(**testversion_attrs)
                
                # TestVersionResults
                xbtestversionresults = xbtestversion.get_results()
                for xbtestversionresult in xbtestversionresults:
                    self.stdout.write("TestVersionResult #%s\n" % xbtestversionresult.id)
                    testversionresult_attr_keys = ('id', 'testversion', 'start_date', 'finished_date', 'status', 'os', 'browser', 'resolution', 'windowed', 'windowed_thumb', 'full_page', 'full_page_thumb', 'live_test_url')
                    try:
                        testversionresult = TestVersionResult.objects.get(id=xbtestversionresult.id)
                        for key in testversionresult_attr_keys:
                            setattr(testversionresult, key, getattr(xbtestversionresult, key))
                            testversionresult.test = test
                        testversionresult.save()
                    except TestVersionResult.DoesNotExist:
                        testversionresult_attrs = dict([(key, getattr(xbtestversionresult, key)) for key in testversionresult_attr_keys])
                        testversionresult_attrs.update(testversion=testversion)
                        testversionresult = TestVersionResult.objects.create(**testversionresult_attrs)
