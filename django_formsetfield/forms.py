
from django.forms import (Form, formset_factory)
from django.forms.fields import CharField

from formsetfield.fields  import FormsetField
from formsetfield.forms import InitFormsetFieldFormMixin

class TestForm(InitFormsetFieldFormMixin,Form):
    name = CharField(max_length= 100)

class TestInlineForm(InitFormsetFieldFormMixin, Form):
    field = CharField(max_length=100)

TestFormset = formset_factory(TestInlineForm, extra=2)

class TestFormsetForm(InitFormsetFieldFormMixin, Form):
    test_forms = FormsetField(formset_class= TestFormset)

TestNestedFormset = formset_factory(TestFormsetForm, extra=2)

class TestNestedFormsetForm(InitFormsetFieldFormMixin, Form):
    title = CharField(max_length=100)
    nested_formset= FormsetField(formset_class=TestNestedFormset)

