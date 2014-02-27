# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ChapterType'
        db.delete_table(u'book_chaptertype')

        # Deleting model 'BookType'
        db.delete_table(u'book_booktype')

        # Deleting model 'Type'
        db.delete_table(u'book_type')

        # Adding model 'Language'
        db.create_table(u'book_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('book', ['Language'])

        # Deleting field 'Chapter.chapter_type'
        db.delete_column(u'book_chapter', 'chapter_type_id')

        # Adding field 'Chapter.language'
        db.add_column(u'book_chapter', 'language',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Language'], null=True),
                      keep_default=False)

        # Deleting field 'Book.ttv_type'
        db.delete_column(u'book_book', 'ttv_type_id')

        # Adding M2M table for field languages on 'Book'
        m2m_table_name = db.shorten_name(u'book_book_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['book.book'], null=False)),
            ('language', models.ForeignKey(orm['book.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'language_id'])


    def backwards(self, orm):
        # Adding model 'ChapterType'
        db.create_table(u'book_chaptertype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('book', ['ChapterType'])

        # Adding model 'BookType'
        db.create_table(u'book_booktype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('book', ['BookType'])

        # Adding model 'Type'
        db.create_table(u'book_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('book', ['Type'])

        # Deleting model 'Language'
        db.delete_table(u'book_language')


        # User chose to not deal with backwards NULL issues for 'Chapter.chapter_type'
        raise RuntimeError("Cannot reverse this migration. 'Chapter.chapter_type' and its values cannot be restored.")
        # Deleting field 'Chapter.language'
        db.delete_column(u'book_chapter', 'language_id')


        # User chose to not deal with backwards NULL issues for 'Book.ttv_type'
        raise RuntimeError("Cannot reverse this migration. 'Book.ttv_type' and its values cannot be restored.")
        # Removing M2M table for field languages on 'Book'
        db.delete_table(db.shorten_name(u'book_book_languages'))


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
        'book.attachment': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Attachment'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Book']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'downloads_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'book.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'book.book': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'books'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['book.Category']"}),
            'chapters_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'complete_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            'favorite_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'favorited_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'favorite_books'", 'symmetrical': 'False', 'through': "orm['book.Favorite']", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'symmetrical': 'False', 'to': "orm['book.Language']"}),
            'last_chapter_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_chapter_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'read_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'read_books'", 'symmetrical': 'False', 'through': "orm['book.UserLog']", 'to': u"orm['auth.User']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'symmetrical': 'False', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'book.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['book.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'book.chapter': {
            'Meta': {'unique_together': "(('book', 'number'),)", 'object_name': 'Chapter'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Book']"}),
            'content': ('ckeditor.fields.RichTextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Language']", 'null': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'thank_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'book.chapterthank': {
            'Meta': {'object_name': 'ChapterThank'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Chapter']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'book.chapterthanksummary': {
            'Meta': {'object_name': 'ChapterThankSummary'},
            'chapter': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['book.Chapter']", 'unique': 'True', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.TextField', [], {})
        },
        'book.copy': {
            'Meta': {'object_name': 'Copy'},
            'book': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['book.Book']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_chapter_number': ('django.db.models.fields.IntegerField', [], {}),
            'last_page': ('django.db.models.fields.IntegerField', [], {}),
            'last_post': ('django.db.models.fields.IntegerField', [], {}),
            'thread_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'book.favorite': {
            'Meta': {'object_name': 'Favorite'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Book']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'book.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'book.profile': {
            'Meta': {'object_name': 'Profile'},
            'chapters_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'daily_approved_attachments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'daily_downloaded_attachments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'daily_uploaded_attachments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_attachments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'book_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'book.rating': {
            'Meta': {'object_name': 'Rating'},
            'average_result': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '2'}),
            'book': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['book.Book']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'book.ratinglog': {
            'Meta': {'object_name': 'RatingLog'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Book']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'book.userlog': {
            'Meta': {'object_name': 'UserLog'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Book']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'page': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['book']