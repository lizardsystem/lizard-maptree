# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.template.defaultfilters import slugify

import factory

from lizard_maptree.models import Category


class CategoryFactory(factory.Factory):
    """Factory for creating Category instances"""
    FACTORY_FOR = Category

    @classmethod
    def _prepare(cls, create, **kwargs):
        name = kwargs.get('name', None)
        category = super(CategoryFactory, cls)._prepare(create, **kwargs)
        if name:
            category.slug = slugify(name)
            if create:
                category.save()
        return category
