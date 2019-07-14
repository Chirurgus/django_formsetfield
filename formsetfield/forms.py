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
                if prefix:
                    new_prefix = prefix + "-" + name
                else:
                    new_prefix = name 
                field.prefix = new_prefix