# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tracker'
        db.create_table(u'limiter_tracker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timeout_module', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timeout_func', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('limit', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'limiter', ['Tracker'])


    def backwards(self, orm):
        # Deleting model 'Tracker'
        db.delete_table(u'limiter_tracker')


    models = {
        u'limiter.tracker': {
            'Meta': {'object_name': 'Tracker'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timeout_func': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeout_module': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['limiter']