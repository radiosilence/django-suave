# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Section'
        db.delete_table('suave_section')

        # Adding model 'Attachment'
        db.create_table('suave_attachment', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('suave', ['Attachment'])


        # Changing field 'Displayable.body'
        db.alter_column('suave_displayable', 'body', self.gf('tinymce.models.HTMLField')())
        # Deleting field 'Page.section'
        db.delete_column('suave_page', 'section_id')

    def backwards(self, orm):
        # Adding model 'Section'
        db.create_table('suave_section', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
            ('url_override', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('suave', ['Section'])

        # Deleting model 'Attachment'
        db.delete_table('suave_attachment')


        # Changing field 'Displayable.body'
        db.alter_column('suave_displayable', 'body', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Page.section'
        raise RuntimeError("Cannot reverse this migration. 'Page.section' and its values cannot be restored.")
    models = {
        'suave.attachment': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Attachment', '_ormbases': ['suave.SiteEntity']},
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.displayable': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Displayable', '_ormbases': ['suave.SiteEntity']},
            'body': ('tinymce.models.HTMLField', [], {}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.page': {
            'Meta': {'ordering': "['order']", 'object_name': 'Page', '_ormbases': ['suave.Displayable']},
            'displayable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.Displayable']", 'unique': 'True', 'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['suave.Page']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'template_override': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'suave.siteentity': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'SiteEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['suave']