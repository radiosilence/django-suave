# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Nav'
        db.create_table('suave_nav', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('suave', ['Nav'])

        # Adding model 'NavItem'
        db.create_table('suave_navitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='navitems', to=orm['suave.Page'])),
            ('nav', self.gf('django.db.models.fields.related.ForeignKey')(related_name='navitems', to=orm['suave.Nav'])),
            ('show_children', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('suave', ['NavItem'])

        # Adding model 'Carousel'
        db.create_table('suave_carousel', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('suave', ['Carousel'])

        # Adding model 'CarouselImage'
        db.create_table('suave_carouselimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suave.Attachment'])),
            ('carousel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suave.Carousel'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('suave', ['CarouselImage'])

        # Adding field 'SiteEntity.identifier'
        db.add_column('suave_siteentity', 'identifier',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Attachment.type'
        db.add_column('suave_attachment', 'type',
                      self.gf('django.db.models.fields.CharField')(default='image', max_length=45),
                      keep_default=False)

        # Adding field 'Attachment.image'
        db.add_column('suave_attachment', 'image',
                      self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Attachment.file'
        db.add_column('suave_attachment', 'file',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'Nav'
        db.delete_table('suave_nav')

        # Deleting model 'NavItem'
        db.delete_table('suave_navitem')

        # Deleting model 'Carousel'
        db.delete_table('suave_carousel')

        # Deleting model 'CarouselImage'
        db.delete_table('suave_carouselimage')

        # Deleting field 'SiteEntity.identifier'
        db.delete_column('suave_siteentity', 'identifier')

        # Deleting field 'Attachment.type'
        db.delete_column('suave_attachment', 'type')

        # Deleting field 'Attachment.image'
        db.delete_column('suave_attachment', 'image')

        # Deleting field 'Attachment.file'
        db.delete_column('suave_attachment', 'file')

    models = {
        'suave.attachment': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Attachment', '_ormbases': ['suave.SiteEntity']},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'image'", 'max_length': '45'})
        },
        'suave.carousel': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Carousel', '_ormbases': ['suave.SiteEntity']},
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'carousels'", 'symmetrical': 'False', 'through': "orm['suave.CarouselImage']", 'to': "orm['suave.Attachment']"}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.carouselimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'CarouselImage'},
            'carousel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suave.Carousel']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suave.Attachment']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'suave.displayable': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Displayable', '_ormbases': ['suave.SiteEntity']},
            'body': ('tinymce.models.HTMLField', [], {}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.nav': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Nav', '_ormbases': ['suave.SiteEntity']},
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'navs'", 'symmetrical': 'False', 'through': "orm['suave.NavItem']", 'to': "orm['suave.Page']"}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.navitem': {
            'Meta': {'ordering': "['order']", 'object_name': 'NavItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nav': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'navitems'", 'to': "orm['suave.Nav']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'navitems'", 'to': "orm['suave.Page']"}),
            'show_children': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['suave']