# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'NavItem.order'
        db.alter_column('suave_navitem', 'order', self.gf('django.db.models.fields.IntegerField')(null=True))
    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'NavItem.order'
        raise RuntimeError("Cannot reverse this migration. 'NavItem.order' and its values cannot be restored.")
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
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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