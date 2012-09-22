# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils.timezone import utc

class Migration(SchemaMigration):

    def forwards(self, orm):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        # Deleting field 'NavItem.show_children'
        db.delete_column('suave_navitem', 'show_children')

        # Adding field 'NavItem.added'
        db.add_column('suave_navitem', 'added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=now, blank=True),
                      keep_default=False)

        # Adding field 'NavItem.updated'
        db.add_column('suave_navitem', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=now, blank=True),
                      keep_default=False)

        # Adding field 'NavItem.type'
        db.add_column('suave_navitem', 'type',
                      self.gf('django.db.models.fields.CharField')(default='page', max_length=15),
                      keep_default=False)

        # Adding field 'NavItem.text'
        db.add_column('suave_navitem', 'text',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True),
                      keep_default=False)

        # Adding field 'NavItem.parent'
        db.add_column('suave_navitem', 'parent',
                      self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['suave.NavItem']),
                      keep_default=False)

        # Adding field 'NavItem.page_show_children'
        db.add_column('suave_navitem', 'page_show_children',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'NavItem.dynamic_name'
        db.add_column('suave_navitem', 'dynamic_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NavItem.dynamic_args'
        db.add_column('suave_navitem', 'dynamic_args',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'NavItem.static_url'
        db.add_column('suave_navitem', 'static_url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NavItem.lft'
        db.add_column('suave_navitem', 'lft',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'NavItem.rght'
        db.add_column('suave_navitem', 'rght',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'NavItem.tree_id'
        db.add_column('suave_navitem', 'tree_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'NavItem.level'
        db.add_column('suave_navitem', 'level',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)


        # Changing field 'NavItem.order'
        db.alter_column('suave_navitem', 'order', self.gf('django.db.models.fields.IntegerField')(null=True))
        # Adding index on 'NavItem', fields ['order']
        db.create_index('suave_navitem', ['order'])


        # Changing field 'NavItem.page'
        db.alter_column('suave_navitem', 'page_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['suave.Page']))

    def backwards(self, orm):
        # Removing index on 'NavItem', fields ['order']
        db.delete_index('suave_navitem', ['order'])

        # Adding field 'NavItem.show_children'
        db.add_column('suave_navitem', 'show_children',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'NavItem.added'
        db.delete_column('suave_navitem', 'added')

        # Deleting field 'NavItem.updated'
        db.delete_column('suave_navitem', 'updated')

        # Deleting field 'NavItem.type'
        db.delete_column('suave_navitem', 'type')

        # Deleting field 'NavItem.text'
        db.delete_column('suave_navitem', 'text')

        # Deleting field 'NavItem.parent'
        db.delete_column('suave_navitem', 'parent_id')

        # Deleting field 'NavItem.page_show_children'
        db.delete_column('suave_navitem', 'page_show_children')

        # Deleting field 'NavItem.dynamic_name'
        db.delete_column('suave_navitem', 'dynamic_name')

        # Deleting field 'NavItem.dynamic_args'
        db.delete_column('suave_navitem', 'dynamic_args')

        # Deleting field 'NavItem.static_url'
        db.delete_column('suave_navitem', 'static_url')

        # Deleting field 'NavItem.lft'
        db.delete_column('suave_navitem', 'lft')

        # Deleting field 'NavItem.rght'
        db.delete_column('suave_navitem', 'rght')

        # Deleting field 'NavItem.tree_id'
        db.delete_column('suave_navitem', 'tree_id')

        # Deleting field 'NavItem.level'
        db.delete_column('suave_navitem', 'level')


        # Changing field 'NavItem.order'
        db.alter_column('suave_navitem', 'order', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'NavItem.page'
        raise RuntimeError("Cannot reverse this migration. 'NavItem.page' and its values cannot be restored.")

    models = {
        'suave.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'image'", 'max_length': '45'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'suave.carousel': {
            'Meta': {'object_name': 'Carousel'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'suave.carouselimage': {
            'Meta': {'object_name': 'CarouselImage'},
            'carousel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suave.Carousel']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'suave.nav': {
            'Meta': {'object_name': 'Nav'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'suave.navitem': {
            'Meta': {'ordering': "['order']", 'object_name': 'NavItem'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dynamic_args': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dynamic_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'nav': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'navitems'", 'to': "orm['suave.Nav']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'navitems'", 'null': 'True', 'to': "orm['suave.Page']"}),
            'page_show_children': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['suave.NavItem']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'static_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'page'", 'max_length': '15'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'suave.page': {
            'Meta': {'ordering': "['order']", 'object_name': 'Page'},
            '_meta_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            '_meta_keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            '_page_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'body': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['suave.Page']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'db_index': 'True'}),
            'template_override': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'suave.redirect': {
            'Meta': {'ordering': "['order']", 'object_name': 'Redirect'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'old_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'permanent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['suave']