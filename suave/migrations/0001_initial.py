# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Displayable'
        db.create_table('suave_displayable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('sort_index', self.gf('django.db.models.fields.IntegerField')()),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('suave', ['Displayable'])

        # Adding model 'Section'
        db.create_table('suave_section', (
            ('displayable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.Displayable'], unique=True, primary_key=True)),
            ('url_override', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('suave', ['Section'])

        # Adding model 'Page'
        db.create_table('suave_page', (
            ('displayable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.Displayable'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages', to=orm['suave.Section'])),
            ('featured_image', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('featured_image_description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('template_override', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('suave', ['Page'])

    def backwards(self, orm):
        # Deleting model 'Displayable'
        db.delete_table('suave_displayable')

        # Deleting model 'Section'
        db.delete_table('suave_section')

        # Deleting model 'Page'
        db.delete_table('suave_page')

    models = {
        'suave.displayable': {
            'Meta': {'object_name': 'Displayable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'sort_index': ('django.db.models.fields.IntegerField', [], {})
        },
        'suave.page': {
            'Meta': {'ordering': "['sort_index']", 'object_name': 'Page', '_ormbases': ['suave.Displayable']},
            'content': ('django.db.models.fields.TextField', [], {}),
            'displayable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.Displayable']", 'unique': 'True', 'primary_key': 'True'}),
            'featured_image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'featured_image_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['suave.Section']"}),
            'template_override': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'suave.section': {
            'Meta': {'ordering': "['sort_index']", 'object_name': 'Section', '_ormbases': ['suave.Displayable']},
            'displayable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.Displayable']", 'unique': 'True', 'primary_key': 'True'}),
            'url_override': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['suave']