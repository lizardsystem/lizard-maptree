lizard-maptree
==========================================

Introduction
------------

Lizard-maptree provides a generic hierarchical tree view for lizard
apps. Put workspace-acceptables in the tree and browse through it.

Usage
-----

Your model must have a ManyToManyField to Category. Also implement a
function in your model names workspace_acceptable. The function should
return a dictionary with the following keys:

- name: display this name in the tree
- type: 'workspace-acceptable'
- description: when not null or empty, displays an 'i' info button
- adapter_layer_json: WorkspaceItem.adapter_layer_json
- adapter_name: adapter name

Example::

    def workspace_acceptable(self):
        return {'name': self.name,
                'type': 'workspace-acceptable',
                'description': self.description,
                'adapter_layer_json': json.dumps({
                    'name': self.name,
                    'url': self.url,
                    'params': self.params,
                    'options': self.options}),
                'adapter_name': ADAPTER_CLASS_WMS}

Finally add urls to your urls.py. Typically::

    url(r'^$',
        'lizard_wms.views.homepage',
        name='lizard_wms.homepage'),
    url(r'^category/(?P<root_slug>.*)/$',
     'lizard_wms.views.homepage',
     name='lizard_wms.homepage'),
    (r'^map/', include('lizard_map.urls')),

Testing
-------

For testing purposes, a dummy workspace-acceptable is added when no
models are associated with Category.
