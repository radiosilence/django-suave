"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from suave.models import *

class TestSuave(TestCase):
    def setUp(self):
        self.home = Page.objects.create(
            title='Home Page',
            slug='home',
            _page_title='Hoooome',
            _meta_keywords='web, site',
            _meta_description='a great website',
        )
        self.page1 = Page.objects.create(
            title='Page One',
            slug='page-1',
            parent=self.home
        )
        self.page1a = Page.objects.create(
            title='Page One (a)',
            slug='a',
            _page_title='One aaye',
            parent=self.page1,
            _meta_keywords='page, one, a',
            _meta_description='the page one of a',
        )
        self.mainnav = NavItem.objects.create(
            type=NavItem.TYPE.menu,
            text='Main Menu',
        )
        self.mainnav_home = NavItem.objects.create(
            type=NavItem.TYPE.page,
            page=self.home,
            parent=self.mainnav
        )
        self.mainnav_pages = NavItem.objects.create(
            type=NavItem.TYPE.menu,
            text='Pages',
            parent=self.mainnav
        )
        self.mainnav_pages_page1 = NavItem.objects.create(
            type=NavItem.TYPE.page,
            page=self.page1,
            text='Page Unos',
            parent=self.mainnav_pages,
        )
        self.mainnav_pages_page1a = NavItem.objects.create(
            type=NavItem.TYPE.dynamic,
            dynamic_name='suave:page',
            dynamic_args='url:page-1/a',
            text='Page One A',
            parent=self.mainnav_pages
        )

    def test_url_home(self):
        self.assertEqual(self.home.url, '/')

    def test_url_page1(self):
        self.assertEqual(self.page1.url, '/page-1/')

    def test_url_page1a(self):
        self.assertEqual(self.page1a.url, '/page-1/a/')

    def test_pagetitle_home(self):
        self.assertEqual(self.home.page_title, 'Hoooome')

    def test_pagetitle_page1(self):
        self.assertEqual(self.page1.page_title, 'Page One')

    def test_pagetitle_page1a(self):
        self.assertEqual(self.page1a.page_title, 'One aaye')

    def test_meta_home(self):
        self.assertEqual(self.home.meta_keywords, 'web, site')
        self.assertEqual(self.home.meta_description, 'a great website')

    def test_meta_page1(self):
        self.assertEqual(self.page1.meta_keywords, 'web, site')
        self.assertEqual(self.page1.meta_description, 'a great website')

    def test_meta_page1a(self):
        self.assertEqual(self.page1a.meta_keywords, 'page, one, a')
        self.assertEqual(self.page1a.meta_description, 'the page one of a')

    def test_nav_home(self):
        self.assertEqual(self.mainnav_home.url, '/')
        self.assertEqual(self.mainnav_home.title, 'Home Page')

    def test_nav_pages(self):
        self.assertEqual(self.mainnav_pages.url, '/page-1/')
        self.assertEqual(self.mainnav_pages.title, 'Pages')

    def test_nav_page1(self):
        self.assertEqual(self.mainnav_pages_page1.title, 'Page Unos')

    def test_nav_page1a(self):
        self.assertEqual(self.mainnav_pages_page1a.url, '/page-1/a/')
        self.assertEqual(self.mainnav_pages_page1a.title, 'Page One A')
