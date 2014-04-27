# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tracker.package'
        db.add_column(u'limiter_tracker', 'package',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tracker.package'
        db.delete_column(u'limiter_tracker', 'package')


    models = {
        u'limiter.tracker': {
            'Meta': {'object_name': 'Tracker'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_func': ('django.db.models.fields.CharField', [], {'default': "'get_user_id'", 'max_length': '255'}),
            'key_module': ('django.db.models.fields.CharField', [], {'default': "'limiter.utils.LimitChecker'", 'max_length': '255'}),
            'limit': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeout_func': ('django.db.models.fields.CharField', [], {'default': "'timeout_to_next_day'", 'max_length': '255'}),
            'timeout_module': ('django.db.models.fields.CharField', [], {'default': "'limiter.utils.LimitChecker'", 'max_length': '255'})
        }
    }

    complete_apps = ['limiter']
