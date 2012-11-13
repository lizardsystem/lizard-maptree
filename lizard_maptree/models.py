# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.db import models
from django.utils.translation import ugettext as _
from treebeard.al_tree import AL_Node


class Category(AL_Node):
    """
    Tree structure for ordering objects.

    Optionally connect shapes to nodes.
    """

    name = models.CharField(
        max_length=80,
        help_text='i.e. max debiet.')
    slug = models.SlugField(
        max_length=20, unique=True)
    parent = models.ForeignKey(
        'Category', null=True, blank=True)

    # For treebeard.
    node_order_by = ['name']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('name', )

    def hierarchy(self):
        """Return string that's useful for sorting and finding categories."""
        return ' -> '.join(['Root'] +
                           [a.slug for a in self.get_ancestors()] +
                           [self.slug])

    def __unicode__(self):
        return self.hierarchy()
