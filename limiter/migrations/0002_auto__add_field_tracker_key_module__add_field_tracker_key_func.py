# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tracker.key_module'
        db.add_column(u'limiter_tracker', 'key_module',
                      self.gf('django.db.models.fields.CharField')(default='limiter.models.Tracker', max_length=255),
                      keep_default=False)

        # Adding field 'Tracker.key_func'
        db.add_column(u'limiter_tracker', 'key_func',
                      self.gf('django.db.models.fields.CharField')(default='get_user_id', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tracker.key_module'
        db.delete_column(u'limiter_tracker', 'key_module')

        # Deleting field 'Tracker.key_func'
        db.delete_column(u'limiter_tracker', 'key_func')


    models = {
        u'limiter.tracker': {
            'Meta': {'object_name': 'Tracker'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_func': ('django.db.models.fields.CharField', [], {'default': "'get_user_id'", 'max_length': '255'}),
            'key_module': ('django.db.models.fields.CharField', [], {'default': "'limiter.models.Tracker'", 'max_length': '255'}),
            'limit': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timeout_func': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeout_module': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['limiter']