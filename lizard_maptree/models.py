# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.core.urlresolvers import reverse
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
    description = models.TextField(null=True, blank=True)
    index = models.IntegerField(default=1000,
        help_text="Number used for ordering categories relative to each other.")
    parent = models.ForeignKey(
        'Category', null=True, blank=True)

    # For treebeard.
    node_order_by = ['index', 'name']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('index', 'name')

    def hierarchy(self):
        """Return string that's useful for sorting and finding categories."""
        return ' -> '.join(['Root'] +
                           [a.slug for a in self.get_ancestors()] +
                           [self.slug])

    def __unicode__(self):
        return self.hierarchy()

    def get_absolute_url(self):
        # We need lizard-wms, as our url is defined there.
        # This is *no* sane separation of apps.
        return reverse('lizard_wms.homepage', kwargs={'root_slug': self.slug})
