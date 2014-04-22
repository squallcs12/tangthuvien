# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Limiter'
        db.create_table(u'limiter_limiter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timeout_func', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('limit', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'limiter', ['Limiter'])


    def backwards(self, orm):
        # Deleting model 'Limiter'
        db.delete_table(u'limiter_limiter')


    models = {
        u'limiter.utils': {
            'Meta': {'object_name': 'Limiter'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {}),
            'timeout_func': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['limiter']