# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Test'
        db.create_table('pagetests_test', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('test_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('pagetests', ['Test'])

        # Adding model 'TestVersion'
        db.create_table('pagetests_testversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pagetests.Test'])),
            ('version_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('count_successful', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('count_not_finished', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('version_public_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('version_ui_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('version_zip', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('w3c_css_errors', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('w3c_html_errors', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('w3c_html_warnings', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('pagetests', ['TestVersion'])

        # Adding model 'TestVersionResult'
        db.create_table('pagetests_testversionresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testversion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pagetests.TestVersion'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('finished_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('browser', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('resolution', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('windowed', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('windowed_thumb', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('full_page', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('full_page_thumb', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('live_test_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('pagetests', ['TestVersionResult'])


    def backwards(self, orm):
        
        # Deleting model 'Test'
        db.delete_table('pagetests_test')

        # Deleting model 'TestVersion'
        db.delete_table('pagetests_testversion')

        # Deleting model 'TestVersionResult'
        db.delete_table('pagetests_testversionresult')


    models = {
        'pagetests.test': {
            'Meta': {'object_name': 'Test'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test_date': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'pagetests.testversion': {
            'Meta': {'object_name': 'TestVersion'},
            'count_not_finished': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'count_successful': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetests.Test']"}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {}),
            'version_public_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version_ui_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version_zip': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'w3c_css_errors': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'w3c_html_errors': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'w3c_html_warnings': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'pagetests.testversionresult': {
            'Meta': {'object_name': 'TestVersionResult'},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'finished_date': ('django.db.models.fields.DateTimeField', [], {}),
            'full_page': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'full_page_thumb': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_test_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'testversion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetests.TestVersion']"}),
            'windowed': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'windowed_thumb': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pagetests']
