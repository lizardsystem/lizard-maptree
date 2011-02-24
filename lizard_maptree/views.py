# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_map.daterange import DateRangeForm
from lizard_map.daterange import current_start_end_dates
from lizard_map.workspace import WorkspaceManager

from lizard_maptree.models import Category


def homepage(request,
             root_slug=None,
             item_models=None,
             javascript_click_handler='popup_click_handler',
             javascript_hover_handler='popup_hover_handler',
             template="lizard_maptree/homepage.html",
             title='',
             sidebar_title='Kaarten'):

    """
    item_models: i.e. ['wmssource', ] (in lower case!) ->
       category.__getattribute__('wmssource_set').all()

       These models must implement the 'workspace_acceptable'
       function, the function returns a dict with keys name, type,
       description, adapter_layer_json, adapter_name.
    """

    def treeitems(category, item_models=None):
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
                       'adapter_name': 'adapter'},]
            return result
        for item_model_name in item_models:
            item_model_set = '%s_set' % item_model_name
            for item in category.__getattribute__(item_model_set).all():
                result.append(item.workspace_acceptable())
        return result

    def get_tree(parent=None, item_models=None):
        """
        Make tree for homepage using Category and Shape.
        """
        result = []
        categories = Category.objects.filter(parent=parent)
        for category in categories:
            # Append sub categories.
            children = get_tree(parent=category, item_models=item_models)
            row = {'name': category.name,
                   'type': 'category',
                   'children': children}
            result.append(row)
        # Append workspace-acceptables.
        if parent is not None:
            result += treeitems(parent, item_models=item_models)
        return result

    parent_category = None
    if root_slug is not None:
        parent_category = get_object_or_404(Category, slug=root_slug)
    tree = get_tree(parent_category, item_models)

    workspace_manager = WorkspaceManager(request)
    workspaces = workspace_manager.load_or_create()
    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))

    context_dict = {
        'javascript_hover_handler': javascript_hover_handler,
        'javascript_click_handler': javascript_click_handler,
        'date_range_form': date_range_form,
        'workspaces': workspaces,
        'tree': tree,
        'parent_category': parent_category,
        'title': title,
        'sidebar_title': sidebar_title}

    return render_to_response(
        template,
        context_dict,
        context_instance=RequestContext(request))
