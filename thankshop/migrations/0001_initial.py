# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserDailyLoginHistory'
        db.create_table(u'thankshop_userdailyloginhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('thankshop', ['UserDailyLoginHistory'])

        # Adding model 'ThankPoint'
        db.create_table(u'thankshop_thankpoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='thank_point', unique=True, to=orm['auth.User'])),
            ('thank_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('thanked_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_thanked_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timeout', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 5, 22, 53, 9, 3))),
        ))
        db.send_create_signal('thankshop', ['ThankPoint'])

        # Adding model 'ThankPointHistory'
        db.create_table(u'thankshop_thankpointhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 5, 22, 53, 9, 3))),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('thankshop', ['ThankPointHistory'])


    def backwards(self, orm):
        # Deleting model 'UserDailyLoginHistory'
        db.delete_table(u'thankshop_userdailyloginhistory')

        # Deleting model 'ThankPoint'
        db.delete_table(u'thankshop_thankpoint')

        # Deleting model 'ThankPointHistory'
        db.delete_table(u'thankshop_thankpointhistory')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'thankshop.thankpoint': {
            'Meta': {'object_name': 'ThankPoint'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_thanked_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thank_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thanked_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timeout': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 5, 22, 53, 9, 3)'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'thank_point'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'thankshop.thankpointhistory': {
            'Meta': {'object_name': 'ThankPointHistory'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 5, 22, 53, 9, 3)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'thankshop.userdailyloginhistory': {
            'Meta': {'object_name': 'UserDailyLoginHistory'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['thankshop']