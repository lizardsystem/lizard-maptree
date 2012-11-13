from django.contrib import admin
from django import forms

from lizard_maptree.models import Category


def category_descendants(obj):
    return ', '.join([a.name for a in obj.get_descendants()])


class ParentCategoryField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.name, obj.slug)


class CategoryForm(forms.ModelForm):
    parent = ParentCategoryField(queryset=Category.objects.all(),
                                 required=False)

    class Meta:
        model = Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'hierarchy', category_descendants)
    list_filter = ('parent', )
    prepopulated_fields = {'slug': ('name',)}
    form = CategoryForm


admin.site.register(Category, CategoryAdmin)
