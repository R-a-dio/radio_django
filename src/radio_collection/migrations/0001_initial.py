# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table(u'radio_collection_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('track', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['radio_collection.Tracks'], unique=True)),
            ('original_filename', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('good', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('uploader_comment', self.gf('django.db.models.fields.CharField')(max_length=120, null=True)),
            ('decline_comment', self.gf('django.db.models.fields.CharField')(max_length=120, null=True)),
        ))
        db.send_create_signal(u'radio_collection', ['Collection'])

        # Adding model 'Tags'
        db.create_table(u'radio_collection_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'radio_collection', ['Tags'])

        # Adding model 'Tracks'
        db.create_table(u'radio_collection_tracks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radio_collection.Artists'], null=True, blank=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radio_collection.Albums'], null=True, blank=True)),
            ('legacy_tags', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'radio_collection', ['Tracks'])

        # Adding M2M table for field tags on 'Tracks'
        db.create_table(u'radio_collection_tracks_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tracks', models.ForeignKey(orm[u'radio_collection.tracks'], null=False)),
            ('tags', models.ForeignKey(orm[u'radio_collection.tags'], null=False))
        ))
        db.create_unique(u'radio_collection_tracks_tags', ['tracks_id', 'tags_id'])

        # Adding model 'Artists'
        db.create_table(u'radio_collection_artists', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'radio_collection', ['Artists'])

        # Adding M2M table for field tags on 'Artists'
        db.create_table(u'radio_collection_artists_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artists', models.ForeignKey(orm[u'radio_collection.artists'], null=False)),
            ('tags', models.ForeignKey(orm[u'radio_collection.tags'], null=False))
        ))
        db.create_unique(u'radio_collection_artists_tags', ['artists_id', 'tags_id'])

        # Adding model 'Albums'
        db.create_table(u'radio_collection_albums', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'radio_collection', ['Albums'])

        # Adding M2M table for field tags on 'Albums'
        db.create_table(u'radio_collection_albums_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('albums', models.ForeignKey(orm[u'radio_collection.albums'], null=False)),
            ('tags', models.ForeignKey(orm[u'radio_collection.tags'], null=False))
        ))
        db.create_unique(u'radio_collection_albums_tags', ['albums_id', 'tags_id'])

        # Adding model 'Played'
        db.create_table(u'radio_collection_played', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radio_collection.Tracks'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'radio_collection', ['Played'])

        # Adding model 'Requests'
        db.create_table(u'radio_collection_requests', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radio_collection.Tracks'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=150, db_index=True)),
        ))
        db.send_create_signal(u'radio_collection', ['Requests'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table(u'radio_collection_collection')

        # Deleting model 'Tags'
        db.delete_table(u'radio_collection_tags')

        # Deleting model 'Tracks'
        db.delete_table(u'radio_collection_tracks')

        # Removing M2M table for field tags on 'Tracks'
        db.delete_table('radio_collection_tracks_tags')

        # Deleting model 'Artists'
        db.delete_table(u'radio_collection_artists')

        # Removing M2M table for field tags on 'Artists'
        db.delete_table('radio_collection_artists_tags')

        # Deleting model 'Albums'
        db.delete_table(u'radio_collection_albums')

        # Removing M2M table for field tags on 'Albums'
        db.delete_table('radio_collection_albums_tags')

        # Deleting model 'Played'
        db.delete_table(u'radio_collection_played')

        # Deleting model 'Requests'
        db.delete_table(u'radio_collection_requests')


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
        u'radio_collection.played': {
            'Meta': {'object_name': 'Played'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radio_collection.Tracks']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'radio_collection.requests': {
            'Meta': {'object_name': 'Requests'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radio_collection.Tracks']"})
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
        }
    }

    complete_apps = ['radio_collection']