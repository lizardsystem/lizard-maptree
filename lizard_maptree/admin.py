from django.contrib import admin

from lizard_maptree.models import Category


def category_ancestors(obj):
    return ' -> '.join(['root'] + [a.name for a in obj.get_ancestors()])


def category_descendants(obj):
    return ', '.join([a.name for a in obj.get_descendants()])


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'slug', category_ancestors,
                    category_descendants)
    list_filter = ('name', 'parent', 'slug', )


admin.site.register(Category, CategoryAdmin)
