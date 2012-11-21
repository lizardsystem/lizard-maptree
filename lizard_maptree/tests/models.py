# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.test import TestCase

from lizard_maptree.models import Category

from factories import CategoryFactory


class CategoryTests(TestCase):

    def test_default_index(self):
        """Tests default index for Category instances"""
        c = CategoryFactory.build(name="drought risk")
        self.assertEquals(c.index, 1000)

    def test_index_based_sorting(self):
        """Tests index based category sorting"""
        parent_1 = CategoryFactory.create(name="parent 1", index=10)
        sub_1 = CategoryFactory.create(name="sub 1", index=13, parent=parent_1)
        sub_2 = CategoryFactory.create(name="sub 2", index=12, parent=parent_1)
        sub_3 = CategoryFactory.create(name="sub 3", index=11, parent=parent_1)
        categories = Category.objects.all()
        indexes = []
        for category in categories:
            indexes.append(category.index)
        self.assertEquals(indexes, sorted(indexes))
        self.assertEquals(categories[0], parent_1)
        self.assertEquals(categories[3], sub_1)

    def test_index_based_sorting_with_two_parents(self):
        """Tests index based category sorting with two parents"""
        parent_2 = CategoryFactory.create(name="parent 2", index=1)
        sub_1a = CategoryFactory.create(name="sub 1a", index=2, parent=parent_2)
        sub_2a = CategoryFactory.create(name="sub 2a", index=4, parent=parent_2)
        sub_3a = CategoryFactory.create(name="sub 3a", index=3, parent=parent_2)
        parent_1 = CategoryFactory.create(name="parent 1", index=10)
        sub_1 = CategoryFactory.create(name="sub 1", index=13, parent=parent_1)
        sub_2 = CategoryFactory.create(name="sub 2", index=12, parent=parent_1)
        sub_3 = CategoryFactory.create(name="sub 3", index=11, parent=parent_1)
        categories = Category.objects.all()
        indexes = []
        for category in categories:
            indexes.append(category.index)
        # first two categories should be the parents in the right order
        self.assertEquals(categories[0], parent_2)
        self.assertEquals(categories[1], parent_1)
