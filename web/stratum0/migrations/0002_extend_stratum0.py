# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Stratum0.project_url'
        db.add_column(u'stratum0_stratum0', 'project_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Stratum0.project_description'
        db.add_column(u'stratum0_stratum0', 'project_description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Stratum0.project_url'
        db.delete_column(u'stratum0_stratum0', 'project_url')

        # Deleting field 'Stratum0.project_description'
        db.delete_column(u'stratum0_stratum0', 'project_description')


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
            'project_description': ('django.db.models.fields.TextField', [], {}),
            'project_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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