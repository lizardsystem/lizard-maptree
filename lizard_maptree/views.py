# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from lizard_ui.layout import Action
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from lizard_map.lizard_widgets import WorkspaceAcceptable
from lizard_map.views import MapView

from lizard_maptree.models import Category


class MaptreeHomepageView(MapView):
    """
    item_models: i.e. ['wmssource', ] (in lower case!) ->
       category.__getattribute__('wmssource_set').all()

       These models must implement the 'workspace_acceptable'
       function, the function returns a dict with keys name, type,
       description, adapter_layer_json, adapter_name.
    """

    template_name = "lizard_maptree/homepage.html"

    item_models = ['wmssource', ]
    _parent_category = None
    _tree = None

    @property
    def root_slug(self):
        return self.kwargs.get('root_slug')

    @property
    def edit_link(self):
        url = reverse('admin:lizard_wms_wmssource_changelist')
        if self.root_slug:
            # We're the root, show all wms sources.
            category = get_object_or_404(Category, slug=self.root_slug)
            url += "?category__id__exact=%s" % category.id
        return url

    @property
    def page_title(self):
        if not self.root_slug:
            return super(MaptreeHomepageView, self).page_title
        return self.parent_category().name

    # Commented it out for the moment: it doesn't work when there's no parent
    # category. It also seems to have logical errors in here.
    # @property
    # def breadcrumbs(self):
    #     according_to_ui = super(MaptreeHomepageView, self).breadcrumbs
    #     if not self.root_slug:
    #         return according_to_ui
    #     category = self.parent_category()
    #     extra = Action(name=category.name)
    #     according_to_ui.append(extra)
    #     return according_to_ui

    def _treeitems(self, category, item_models=None):
        """
        result = [{'name': 'testname',
        'workspace-type': 'workspace-acceptable',
        'description': 'description',
        'adapter_layer_json': '"json"',
        'adapter_name': 'adapter'},]
        """
        result = []
        if item_models is None:
            # Add dummy
            result = [WorkspaceAcceptable(
                    name='workspace-acceptable',
                    adapter_layer_json='"json"',
                    adapter_name='adapter',
                    description='description')]
            return result
        for item_model_name in item_models:
            item_model_set = '%s_set' % item_model_name
            for item in category.__getattribute__(item_model_set).all():
                result.append(item.workspace_acceptable())
        return result

    def _get_tree(self, parent=None, item_models=None, heading_level=2):
        """
        Make tree for homepage using Category and Shape.
        """
        result = []
        heading = 'h%s' % heading_level
        categories = Category.objects.filter(parent=parent)
        for category in categories:
            # Append sub categories.
            children = self._get_tree(parent=category,
                                      item_models=item_models,
                                      heading_level=heading_level + 1)
            row = {'name': category.name,
                   'workspace_type': 'category',
                   'heading': heading,
                   'description': category.description,
                   'children': children}
            result.append(row)
        # Append workspace-acceptables.
        if parent is not None:
            result += self._treeitems(parent, item_models=item_models)
        return result

    def parent_category(self):
        if self._parent_category is None:
            if self.root_slug is not None:
                self._parent_category = get_object_or_404(
                    Category, slug=self.root_slug)
        return self._parent_category

    def tree(self):
        if self._tree is None:
            self._tree = self._get_tree(self.parent_category(),
                                        self.item_models)
        return self._tree
