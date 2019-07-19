from django.forms import Form

from .fields import FormsetField

class InitFormsetFieldFormMixin(object):
    '''
    Sets the prefix for the FormsetField,
    so that when a form with a FormsetField
    it itself put into a formset there are
    no naming/id conflicts.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, FormsetField):
                field.prefix = self.add_prefix(name)

class ModelFormsetFieldFormMixin(InitFormsetFieldFormMixin):
    '''
    '''
    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(field, FormsetField):
                field.instance = instance
    
    def save(self, commit):
        instance = super().save(commit)
        for name, field in self.fields.items():
            if isinstance(field, FormsetField):
                self.cleaned_data[name].instance = instance
                self.cleaned_data[name].save(commit)
        return instance


    def is_valid(self):
        valid = super().is_valid()
        for name, field in self.fields.items():
            if isinstance(field, FormsetField):
                valid = self.cleaned_data[name].is_valid() and valid 
        return valid
    
