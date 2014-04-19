# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Feedback.ip'
        db.add_column(u'feedback_feedback', 'ip',
                      self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Feedback.ip'
        db.delete_column(u'feedback_feedback', 'ip')


    models = {
        u'feedback.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'})
        }
    }

    complete_apps = ['feedback']