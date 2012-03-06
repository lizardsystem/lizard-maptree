# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.shortcuts import get_object_or_404
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
    edit_link = '/admin/lizard_wms/wmssource/'

    javascript_hover_handler = 'popup_hover_handler'
    javascript_click_handler = 'popup_click_handler'
    sidebar_title = 'Kaarten'
    root_slug = None
    item_models = ['wmssource', ]
    _parent_category = None
    _tree = None

    def _treeitems(self, category, item_models=None):
        """
        result = [{'name': 'testname',
        'type': 'workspace-acceptable',
        'description': 'description',
        'adapter_layer_json': '"json"',
        'adapter_name': 'adapter'},]
        """
        result = []
        if item_models is None:
            # Add dummy
            result = [{'name': 'dummy workspace-acceptable',
                       'type': 'workspace-acceptable',
                       'description': 'description',
                       'adapter_layer_json': '"json"',
                       'adapter_name': 'adapter'}, ]
            return result
        for item_model_name in item_models:
            item_model_set = '%s_set' % item_model_name
            for item in category.__getattribute__(item_model_set).all():
                result.append(item.workspace_acceptable())
        return result

    def _get_tree(self, parent=None, item_models=None):
        """
        Make tree for homepage using Category and Shape.
        """
        result = []
        categories = Category.objects.filter(parent=parent)
        for category in categories:
            # Append sub categories.
            children = self._get_tree(parent=category, item_models=item_models)
            row = {'name': category.name,
                   'type': 'category',
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
