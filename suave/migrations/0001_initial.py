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
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
        ))
        db.send_create_signal('suave', ['SiteEntity'])

        # Adding model 'Displayable'
        db.create_table('suave_displayable', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
            ('body', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal('suave', ['Displayable'])

        # Adding model 'Attachment'
        db.create_table('suave_attachment', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='image', max_length=45)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('suave', ['Attachment'])

        # Adding model 'Page'
        db.create_table('suave_page', (
            ('displayable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.Displayable'], unique=True, primary_key=True)),
            ('template_override', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['suave.Page'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('suave', ['Page'])

        # Adding model 'Carousel'
        db.create_table('suave_carousel', (
            ('siteentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suave.SiteEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('suave', ['Carousel'])

        # Adding model 'CarouselImage'
        db.create_table('suave_carouselimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('carousel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suave.Carousel'])),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('suave', ['CarouselImage'])

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
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('suave', ['NavItem'])

    def backwards(self, orm):
        # Deleting model 'SiteEntity'
        db.delete_table('suave_siteentity')

        # Deleting model 'Displayable'
        db.delete_table('suave_displayable')

        # Deleting model 'Attachment'
        db.delete_table('suave_attachment')

        # Deleting model 'Page'
        db.delete_table('suave_page')

        # Deleting model 'Carousel'
        db.delete_table('suave_carousel')

        # Deleting model 'CarouselImage'
        db.delete_table('suave_carouselimage')

        # Deleting model 'Nav'
        db.delete_table('suave_nav')

        # Deleting model 'NavItem'
        db.delete_table('suave_navitem')

    models = {
        'suave.attachment': {
            'Meta': {'ordering': "['order']", 'object_name': 'Attachment', '_ormbases': ['suave.SiteEntity']},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'image'", 'max_length': '45'})
        },
        'suave.carousel': {
            'Meta': {'ordering': "['order']", 'object_name': 'Carousel', '_ormbases': ['suave.SiteEntity']},
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.carouselimage': {
            'Meta': {'object_name': 'CarouselImage'},
            'carousel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suave.Carousel']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'suave.displayable': {
            'Meta': {'ordering': "['order']", 'object_name': 'Displayable', '_ormbases': ['suave.SiteEntity']},
            'body': ('tinymce.models.HTMLField', [], {}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.nav': {
            'Meta': {'ordering': "['order']", 'object_name': 'Nav', '_ormbases': ['suave.SiteEntity']},
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'navs'", 'symmetrical': 'False', 'through': "orm['suave.NavItem']", 'to': "orm['suave.Page']"}),
            'siteentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suave.SiteEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'suave.navitem': {
            'Meta': {'ordering': "['order']", 'object_name': 'NavItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nav': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'navitems'", 'to': "orm['suave.Nav']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'Meta': {'ordering': "['order']", 'object_name': 'SiteEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['suave']