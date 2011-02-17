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
             item_classes=None,
             javascript_click_handler='popup_click_handler',
             javascript_hover_handler='popup_hover_handler',
             template="lizard_maptree/homepage.html"):

    def treeitems(item_classes=None):
        """
        result = [{'name': 'testname',
        'type': 'workspace-acceptable',
        'description': 'description',
        'adapter_layer_json': '"json"',
        'adapter_name': 'adapter'},]
        """
        if item_classes is None:
            # Add dummy
            result = [{'name': 'dummy workspace-acceptable',
                       'type': 'workspace-acceptable',
                       'description': 'description',
                       'adapter_layer_json': '"json"',
                       'adapter_name': 'adapter'},]
        return result

    def get_tree(parent=None, item_classes=None):
        """
        Make tree for homepage using Category and Shape.
        """
        result = []
        categories = Category.objects.filter(parent=parent)
        for category in categories:
            # Append sub categories.
            children = get_tree(parent=category)
            row = {'name': category.name,
                   'type': 'category',
                   'children': children}
            result.append(row)
        if parent is not None:
            result += treeitems(item_classes=item_classes)
        return result

    parent_category = None
    if root_slug is not None:
        parent_category = get_object_or_404(Category, slug=root_slug)
    tree = get_tree(parent_category, item_classes)

    workspace_manager = WorkspaceManager(request)
    workspaces = workspace_manager.load_or_create()
    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))

    return render_to_response(
        template,
        {'javascript_hover_handler': javascript_hover_handler,
         'javascript_click_handler': javascript_click_handler,
         'date_range_form': date_range_form,
         'workspaces': workspaces,
         'tree': tree,
         'parent_category': parent_category},
        context_instance=RequestContext(request))
