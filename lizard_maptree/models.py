# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.db import models
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
        ordering = ('name', )

    def __unicode__(self):
        return '%s' % (self.name)
