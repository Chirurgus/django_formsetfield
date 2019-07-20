
from django.forms import (Form, formset_factory, ModelForm, inlineformset_factory,)
from django.forms.fields import CharField

from formsetfield.fields  import FormsetField, ModelFormsetField
from formsetfield.forms import InitFormsetFieldFormMixin, ModelFormsetFieldFormMixin

from .models import Recipe, Ingredient

class TestForm(InitFormsetFieldFormMixin,Form):
    name = CharField(max_length= 100)

class TestInlineForm(InitFormsetFieldFormMixin, Form):
    field = CharField(max_length=10)

TestFormset = formset_factory(TestInlineForm, extra=2)

class TestFormsetForm(InitFormsetFieldFormMixin, Form):
    test_forms = FormsetField(formset_class= TestFormset)

TestNestedFormset = formset_factory(TestFormsetForm, extra=2)

class TestNestedFormsetForm(InitFormsetFieldFormMixin, Form):
    title = CharField(max_length=100)
    nested_formset= FormsetField(formset_class=TestNestedFormset)

class TestIngredientForm(ModelFormsetFieldFormMixin, ModelForm):
    class Meta:
        model= Ingredient
        fields= ['ingredient']

IngredientFormset = inlineformset_factory(Recipe, Ingredient, form= TestIngredientForm, extra=3)

class TestRecipeForm(ModelFormsetFieldFormMixin, ModelForm):
    ingredients = ModelFormsetField(formset_class=IngredientFormset)

    class Meta:
        model= Recipe
        fields= ['name']
