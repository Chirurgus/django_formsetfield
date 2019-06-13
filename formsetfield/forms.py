from django.forms import Form

from .fields import FormsetField

class InitFormsetFieldFormMixin(object):
    def __init__(self, prefix=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(field, FormsetField):
                field.prefix = prefix