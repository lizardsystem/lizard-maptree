from django.contrib import admin
from django import forms

from lizard_maptree.models import Category

def category_ancestors(obj):
    return ' -> '.join(['root'] + [a.slug for a in obj.get_ancestors()])

def category_descendants(obj):
    return ', '.join([a.name for a in obj.get_descendants()])

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.name, obj.slug)

class CategoryForm(forms.ModelForm):
    parent = CustomModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'slug', category_ancestors,
                    category_descendants)
    list_filter = ('name', 'parent', 'slug', )
    form = CategoryForm

admin.site.register(Category, CategoryAdmin)
