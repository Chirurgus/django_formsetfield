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
                # Need to update field instance since it still refences
                # the field from which it was initialized (i.e. the field 
                # from self.base_fields)
                field.widget.field_instance = field

class ModelFormsetFieldFormMixin(InitFormsetFieldFormMixin):
    '''
    '''
    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, FormsetField):
                field.instance = instance
                
    
    def save(self, commit=True):
        instance = super().save(commit)
        for name, field in self.fields.items():
            if isinstance(field, FormsetField):
                self.cleaned_data[name].instance = instance
                self.cleaned_data[name].save(commit)
        return instance

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return False
        instance = self.save(commit=False)
        for name, field in self.fields.items():
            if isinstance(field, FormsetField):
                # Set the instance so that
                # the .is_valid method can work
                self.cleaned_data[name].instance = instance
                valid = valid and self.cleaned_data[name].is_valid()
        return valid
