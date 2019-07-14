from django.forms import Form

from .fields import FormsetField

class InitFormsetFieldFormMixin(object):
    '''
    Sets the prefix for the FormsetField,
    so that when a form with a FormsetField
    it itself put into a formset there are
    no naming/id conflicts.
    '''
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, prefix=prefix, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, FormsetField):
                field.prefix = self.add_prefix(name)