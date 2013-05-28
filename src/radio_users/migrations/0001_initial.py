# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Djs'
        db.create_table(u'radio_users_djs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='dj_account', unique=True, to=orm['auth.User'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'radio_users', ['Djs'])

        # Adding model 'Nicknames'
        db.create_table(u'radio_users_nicknames', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('passcode', self.gf('django.db.models.fields.CharField')(max_length=8, null=True)),
        ))
        db.send_create_signal(u'radio_users', ['Nicknames'])

        # Adding model 'Names'
        db.create_table(u'radio_users_names', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('nickname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radio_users.Nicknames'])),
        ))
        db.send_create_signal(u'radio_users', ['Names'])

        # Adding model 'Faves'
        db.create_table(u'radio_users_faves', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radio_users.Names'])),
        ))
        db.send_create_signal(u'radio_users', ['Faves'])

        # Adding model 'Uploads'
        db.create_table(u'radio_users_uploads', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('upload', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radio_collection.Collection'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'radio_users', ['Uploads'])


    def backwards(self, orm):
        # Deleting model 'Djs'
        db.delete_table(u'radio_users_djs')

        # Deleting model 'Nicknames'
        db.delete_table(u'radio_users_nicknames')

        # Deleting model 'Names'
        db.delete_table(u'radio_users_names')

        # Deleting model 'Faves'
        db.delete_table(u'radio_users_faves')

        # Deleting model 'Uploads'
        db.delete_table(u'radio_users_uploads')


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
        u'radio_collection.albums': {
            'Meta': {'object_name': 'Albums'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['radio_collection.Tags']", 'null': 'True', 'blank': 'True'})
        },
        u'radio_collection.artists': {
            'Meta': {'object_name': 'Artists'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['radio_collection.Tags']", 'null': 'True', 'blank': 'True'})
        },
        u'radio_collection.collection': {
            'Meta': {'object_name': 'Collection'},
            'decline_comment': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_filename': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'track': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['radio_collection.Tracks']", 'unique': 'True'}),
            'uploader_comment': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'})
        },
        u'radio_collection.tags': {
            'Meta': {'object_name': 'Tags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'radio_collection.tracks': {
            'Meta': {'object_name': 'Tracks'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radio_collection.Albums']", 'null': 'True', 'blank': 'True'}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radio_collection.Artists']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_tags': ('django.db.models.fields.TextField', [], {}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['radio_collection.Tags']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'radio_users.djs': {
            'Meta': {'object_name': 'Djs'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'dj_account'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'radio_users.faves': {
            'Meta': {'object_name': 'Faves'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radio_users.Names']"})
        },
        u'radio_users.names': {
            'Meta': {'object_name': 'Names'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'nickname': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radio_users.Nicknames']"})
        },
        u'radio_users.nicknames': {
            'Meta': {'object_name': 'Nicknames'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'})
        },
        u'radio_users.uploads': {
            'Meta': {'object_name': 'Uploads'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radio_collection.Collection']"})
        }
    }

    complete_apps = ['radio_users']