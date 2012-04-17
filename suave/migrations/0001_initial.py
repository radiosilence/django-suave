# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteEntity'
        db.create_table('suave_siteentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
        ))
        db.send_create_signal('suave', ['SiteEntity'])

        # Adding model 'Displayable'
        db.create_table('suave_displayable', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('suave', ['Displayable'])

        # Adding model 'Section'
        db.create_table('suave_section', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
            ('url_override', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('suave', ['Section'])

        # Adding model 'Page'
        db.create_table('suave_page', (
            ('displayable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.Displayable'], unique=True, primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages', to=orm['suave.Section'])),
            ('featured_image', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('featured_image_description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('template_override', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['suave.Page'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('suave', ['Page'])

    def backwards(self, orm):
        # Deleting model 'SiteEntity'
        db.delete_table('suave_siteentity')

        # Deleting model 'Displayable'
        db.delete_table('suave_displayable')

        # Deleting model 'Section'
        db.delete_table('suave_section')

        # Deleting model 'Page'
        db.delete_table('suave_page')

    models = {
        'suave.displayable': {
            'Meta': {'object_name': 'Displayable', '_ormbases': ['suave.SiteEntity']},
            'body': ('django.db.models.fields.TextField', [], {}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.page': {
            'Meta': {'ordering': "['order']", 'object_name': 'Page', '_ormbases': ['suave.Displayable']},
            'displayable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.Displayable']", 'unique': 'True', 'primary_key': 'True'}),
            'featured_image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'featured_image_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['suave']