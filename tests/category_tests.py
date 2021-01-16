# -*- coding: utf-8 -*-
"""Tests for the Category class."""
#
# (C) Pywikibot team, 2014-2019
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, division, unicode_literals

import pywikibot
import pywikibot.page

from tests.aspects import unittest, TestCase


class TestCategoryObject(TestCase):

    """Test Category object."""

    NOCATEGORYNAMESPACE_RE = "'(.*?)' is not in the category namespace!"
    NOREDIRECTPAGE_RE = r'Page \[\[(.*?)\]\] is not a redirect page.'

    family = 'wikipedia'
    code = 'en'

    cached = True

    def test_init(self):
        """Test the category's __init__ for one condition that can't be dry."""
        site = self.get_site()
        self.assertRaisesRegex(ValueError, self.NOCATEGORYNAMESPACE_RE,
                               pywikibot.Category, site, 'Wikipedia:Test')

    def test_is_empty(self):
        """Test if category is empty or not."""
        site = self.get_site()
        cat_empty = pywikibot.Category(site, 'Category:foooooo')
        cat_not_empty = pywikibot.Category(site,
                                           'Category:Wikipedia categories')
        self.assertTrue(cat_empty.isEmptyCategory())
        self.assertFalse(cat_not_empty.isEmptyCategory())

    def test_is_hidden(self):
        """Test isHiddenCategory."""
        site = self.get_site()
        cat_hidden = pywikibot.Category(site, 'Category:Hidden categories')
        cat_not_hidden = pywikibot.Category(site, 'Category:Wikipedia')
        self.assertTrue(cat_hidden.isHiddenCategory())
        self.assertFalse(cat_not_hidden.isHiddenCategory())

    def test_categoryinfo(self):
        """Test the categoryinfo property."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Female Wikipedians')
        categoryinfo = cat.categoryinfo
        self.assertGreaterEqual(categoryinfo['files'], 0)
        self.assertGreaterEqual(categoryinfo['pages'], 0)
        self.assertGreater(categoryinfo['size'], 0)
        self.assertGreater(categoryinfo['subcats'], 0)
        members_sum = (categoryinfo['files'] + categoryinfo['pages']
                       + categoryinfo['subcats'])
        self.assertEqual(members_sum, categoryinfo['size'])

        cat_files = pywikibot.Category(site,
                                       'Category:Files lacking an author')
        categoryinfo2 = cat_files.categoryinfo
        self.assertGreater(categoryinfo2['files'], 0)

    def test_members(self):
        """Test the members method."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Wikipedia legal policies')
        p1 = pywikibot.Page(site, 'Category:Wikipedia disclaimers')
        p2 = pywikibot.Page(site, 'Wikipedia:Privacy policy')
        p3 = pywikibot.Page(site, 'Wikipedia:Risk disclaimer')

        members = list(cat.members())
        self.assertIn(p1, members)
        self.assertIn(p2, members)
        self.assertNotIn(p3, members)

        members_recurse = list(cat.members(recurse=True))
        self.assertIn(p1, members_recurse)
        self.assertIn(p2, members_recurse)
        self.assertIn(p3, members_recurse)

        members_namespace = list(cat.members(namespaces=14))
        self.assertIn(p1, members_namespace)
        self.assertNotIn(p2, members_namespace)
        self.assertNotIn(p3, members_namespace)

        members_total = list(cat.members(total=2))
        self.assertLength(members_total, 2)

    def test_subcategories(self):
        """Test the subcategories method."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Wikipedians by gender')
        c1 = pywikibot.Category(site, 'Category:Female Wikipedians')
        c2 = pywikibot.Category(site, 'Category:Lesbian Wikipedians')

        subcategories = list(cat.subcategories())
        self.assertIn(c1, subcategories)
        self.assertNotIn(c2, subcategories)

        subcategories_total = list(cat.subcategories(total=2))
        self.assertLength(subcategories_total, 2)

    def test_subcategories_recurse(self):
        """Test the subcategories method with recurse=True."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Wikipedians by gender')
        c1 = pywikibot.Category(site, 'Category:Female Wikipedians')
        c2 = pywikibot.Category(site, 'Category:Lesbian Wikipedians')

        subcategories_recurse = list(cat.subcategories(recurse=True))
        self.assertIn(c1, subcategories_recurse)
        self.assertIn(c2, subcategories_recurse)

    def test_articles(self):
        """Test the articles method."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Wikipedia legal policies')
        p1 = pywikibot.Page(site, 'Wikipedia:Privacy policy')
        p2 = pywikibot.Page(site, 'Wikipedia:Risk disclaimer')

        articles = list(cat.articles())
        self.assertIn(p1, articles)
        self.assertNotIn(p2, articles)

        articles_recurse = list(cat.articles(recurse=True))
        self.assertIn(p1, articles_recurse)
        self.assertIn(p2, articles_recurse)

        articles_namespace = list(cat.articles(namespaces=1))
        self.assertNotIn(p1, articles_namespace)
        self.assertNotIn(p2, articles_namespace)

        articles_total = list(cat.articles(total=2))
        self.assertLength(articles_total, 2)

    def test_redirects(self):
        """Test the redirects method."""
        site = self.get_site()
        cat1 = pywikibot.Category(site, 'Category:Fonts')
        cat2 = pywikibot.Category(site, 'Category:Typefaces')

        self.assertTrue(cat1.isCategoryRedirect())
        self.assertFalse(cat2.isCategoryRedirect())

        # The correct target category if fetched.
        tgt = cat1.getCategoryRedirectTarget()
        self.assertEqual(tgt, cat2)

        # Raise exception if target is fetched for non Category redirects.
        self.assertRaisesRegex(pywikibot.IsNotRedirectPage,
                               self.NOREDIRECTPAGE_RE,
                               cat2.getCategoryRedirectTarget)


class TestCategoryDryObject(TestCase):

    """Test the category object with dry tests."""

    NOCATEGORYNAMESPACE_RE = "'(.*?)' is not in the category namespace!"

    family = 'wikipedia'
    code = 'en'

    dry = True

    def test_init_dry(self):
        """Test the category's __init__."""
        site = self.get_site()
        cat_normal = pywikibot.Category(site, 'Category:Foo')
        self.assertEqual(cat_normal.title(with_ns=False), 'Foo')
        self.assertEqual(cat_normal.namespace(), 14)

        cat_missing = pywikibot.Category(site, 'Foo')
        self.assertEqual(cat_missing.title(with_ns=False), 'Foo')
        self.assertEqual(cat_missing.namespace(), 14)

        cat_duplicate = pywikibot.Category(site, 'Category:Category:Foo')
        self.assertEqual(cat_duplicate.title(with_ns=False), 'Category:Foo')
        self.assertEqual(cat_duplicate.namespace(), 14)

        cat_dup_ns = pywikibot.Category(site, 'Category:Wikipedia:Test')
        self.assertTrue(cat_dup_ns.title(with_ns=False), 'Page:Foo')
        self.assertTrue(cat_dup_ns.namespace(), 14)

        self.assertRaisesRegex(ValueError, self.NOCATEGORYNAMESPACE_RE,
                               pywikibot.Category, site, 'Talk:Foo')

    def test_section(self):
        """Test the section method."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Foo#bar')
        self.assertEqual(cat.section(), 'bar')
        cat2 = pywikibot.Category(site, 'Category:Foo')
        self.assertIsNone(cat2.section())

    def test_aslink(self):
        """Test the title method with as_link=True."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Wikipedia Categories')
        self.assertEqual(cat.title(as_link=True, insite=cat.site),
                         '[[Category:Wikipedia Categories]]')
        cat_section = pywikibot.Category(site,
                                         'Category:Wikipedia Categories#Foo')
        self.assertEqual(
            cat_section.title(as_link=True, insite=cat_section.site),
            '[[Category:Wikipedia Categories#Foo]]')
        cat_dup = pywikibot.Category(site, 'Category:Wikipedia:Test')
        self.assertEqual(cat_dup.title(as_link=True, insite=cat_dup.site),
                         '[[Category:Wikipedia:Test]]')

    def test_sortkey(self):
        """Test the sortKey attribute."""
        site = self.get_site()
        cat = pywikibot.Category(site, 'Category:Wikipedia categories',
                                 'Example')
        self.assertEqual(cat.aslink(),
                         '[[Category:Wikipedia categories|Example]]')
        self.assertEqual(cat.aslink(sort_key='Foo'),
                         '[[Category:Wikipedia categories|Foo]]')


class CategoryNewestPages(TestCase):

    """Test newest_pages feature on French Wikinews."""

    family = 'wikinews'
    code = 'fr'

    cached = True

    def test_newest_pages(self):
        """Test that the pages are getting older."""
        cat = pywikibot.Category(self.get_site(), 'Catégorie:Yukon Quest 2015')
        last = pywikibot.Timestamp.max
        count = 0
        for page in cat.newest_pages():
            creation_stamp = page.oldest_revision.timestamp
            self.assertLessEqual(creation_stamp, last)
            last = creation_stamp
            count += 1
        self.assertEqual(count, cat.categoryinfo['size'])


if __name__ == '__main__':  # pragma: no cover
    try:
        unittest.main()
    except SystemExit:
        pass
