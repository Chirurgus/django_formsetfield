""" Created by Oleksandr Sorocynskyi """
""" On 26/05/2019 """

from django.forms.fields import Field

from .widgets import FormsetWidget, ModelFormsetWidget

class FormsetField(Field):
    """
    Allows to have a formset as a field in a form.

    Has to be used inside a Formclass deriving from
    @class(FormsetFieldFormMixin).

    The trickiest part of the implementation is 
    having correct id/names for the forms in the
    formset.
    This is accomplished by having the form set
    the self.prefix property with the name of the
    field + prefix from the enclosing formset (if any).
    This is done in the FormsetFieldFormMixin, hence
    the requirement to be in a form deriving form it.
    """
    widget_class = FormsetWidget
    
    # initial = the formset
    # _initial = the initial argument to the formset
    _initial = None

    def __init__(self, *, formset_class, **kwargs):
        # Ignore 'initial' argument, we handle it ourselves
        self._initial = kwargs.pop('initial', None)

        # Instantiate the widget, passing it 'self'
        # so that it can retrieve an update prefix
        widget = kwargs.pop('widget', None)
        if widget is None or isinstance(widget, type) :
            # Ignore the passed widget class
            widget = self.widget_class(field_instance=self)
        else:
            if not isinstance(widget, self.widget_class):
                raise TypeError("widget has to be an instance of FormsetWidget")
            else:
                widget.field_instance = self

        # Super will assign self.widget
        super().__init__(widget=widget,**kwargs)
        # Save formset_class
        self.formset_class = formset_class

    @property
    def initial(self):
        '''
        Returns the inital formset instance.
        This needs to be a method since we need to push back
        the formset instantiation as late as possible so 
        that the self.prefix property is set by the 
        form mixin __init__ (which happens only when the
        form is instantiated in a view).
        '''
        return self.formset_class(prefix=self.prefix, initial=self._initial)
    
    @initial.setter
    def initial(self, val):
        '''
        Set '_initial' property. It is passed to the self.formset_class
        as the 'initial' argument.
        '''
        pass

    def clean(self, value):
        '''
        Return clean value from the raw value extracted from the widget.
        '''
        # value should just be a Formset with data
        # All we need to do is force clean
        value.is_valid()
        return value
  
    def to_python(self, value):
        ''' 
        Return a Django Formset instance.
        '''
        # value should already be a Formset with data
        return value

class ModelFormsetField(FormsetField):
    widget_class = ModelFormsetWidget
    # Instance of the model. Set from ModelFormsetFieldFormMixin.__init__.
    instance = None

    @property
    def initial(self):
        '''
        Same as FormsetField.initial(), but also passes the model
        instance.
        '''
        return self.formset_class(instance=self.instance, prefix=self.prefix)
    
    @initial.setter
    def initial(self, value):
        pass
