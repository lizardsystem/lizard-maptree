lizard-maptree
==========================================

Introduction

Lizard-maptree provides a generic hierarchical tree view for lizard
apps. Put workspace-acceptables in the tree and browse through it.

Usage

Your model must have a ManyToManyField to Category. Also implement a
function in your model names workspace_acceptable. The function should
return a dictionary with the following keys:

- name: display this name in the tree
- type: 'workspace-acceptable'
- description: when not null or empty, displays an 'i' info button
- adapter_layer_json: WorkspaceItem.adapter_layer_json
- adapter_name: adapter name
