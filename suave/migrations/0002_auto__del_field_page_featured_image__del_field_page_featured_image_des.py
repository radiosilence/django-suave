# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Page.featured_image'
        db.delete_column('suave_page', 'featured_image')

        # Deleting field 'Page.featured_image_description'
        db.delete_column('suave_page', 'featured_image_description')

    def backwards(self, orm):
        # Adding field 'Page.featured_image'
        db.add_column('suave_page', 'featured_image',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.featured_image_description'
        db.add_column('suave_page', 'featured_image_description',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

    models = {
        'suave.displayable': {
            'Meta': {'object_name': 'Displayable', '_ormbases': ['suave.SiteEntity']},
            'body': ('django.db.models.fields.TextField', [], {}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.page': {
            'Meta': {'ordering': "['order']", 'object_name': 'Page', '_ormbases': ['suave.Displayable']},
            'displayable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.Displayable']", 'unique': 'True', 'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['suave.Page']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['suave.Section']"}),
            'template_override': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'suave.section': {
            'Meta': {'ordering': "['order']", 'object_name': 'Section', '_ormbases': ['suave.SiteEntity']},
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'}),
            'url_override': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'suave.siteentity': {
            'Meta': {'object_name': 'SiteEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['suave']