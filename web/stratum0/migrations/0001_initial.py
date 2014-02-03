# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReplicationSite'
        db.create_table(u'stratum0_replicationsite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'stratum0', ['ReplicationSite'])

        # Adding model 'Stratum0'
        db.create_table(u'stratum0_stratum0', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fqrn', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'stratum0', ['Stratum0'])

        # Adding model 'Stratum1'
        db.create_table(u'stratum0_stratum1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stratum0', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stratum0.Stratum0'])),
            ('replication_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stratum0.ReplicationSite'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'stratum0', ['Stratum1'])


    def backwards(self, orm):
        # Deleting model 'ReplicationSite'
        db.delete_table(u'stratum0_replicationsite')

        # Deleting model 'Stratum0'
        db.delete_table(u'stratum0_stratum0')

        # Deleting model 'Stratum1'
        db.delete_table(u'stratum0_stratum1')


    models = {
        u'stratum0.replicationsite': {
            'Meta': {'object_name': 'ReplicationSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stratum0.stratum0': {
            'Meta': {'object_name': 'Stratum0'},
            'fqrn': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'stratum0.stratum1': {
            'Meta': {'object_name': 'Stratum1'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'replication_site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stratum0.ReplicationSite']"}),
            'stratum0': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stratum0.Stratum0']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['stratum0']