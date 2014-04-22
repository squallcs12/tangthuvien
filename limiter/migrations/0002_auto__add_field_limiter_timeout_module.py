# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Limiter.timeout_module'
        db.add_column(u'limiter_limiter', 'timeout_module',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Limiter.timeout_module'
        db.delete_column(u'limiter_limiter', 'timeout_module')


    models = {
        u'limiter.utils': {
            'Meta': {'object_name': 'Limiter'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {}),
            'timeout_func': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeout_module': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['limiter']