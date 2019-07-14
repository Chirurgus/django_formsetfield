""" Created by Oleksandr Sorocynskyi """
""" On 26/05/2019 """

from django.forms.widgets import Widget

class FormsetWidget(Widget):
    '''
    Displays a formset.

    Meant to be used only with FormsetField, since
    it has very close coupling with it.
    Notably FormsetField passes its own instance
    to this widget so that this widget can get
    up-to-date information about what prefix
    to use. This is necessary since the correct
    prefix is not known on __init__ time.
    '''
    template_name = 'formsetwidget/formset.html'
    needs_multipart_form = True

    def __init__(self, *args, field_instance, **kwargs):
        self.field_instance = field_instance
        super(FormsetWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        '''
        Extract value from HTML request data, and files,
        given the widget's name.
        The value in this case is a Django FormSet.
        '''
        # Return the formset populated with data
        return self.field_instance.formset_class(
            data,
            files,
            prefix= name) # the name is generated using add_prefix(name)
                          # same way we generate the prefix, so we can 
                          # use it to access the right formset, without
                          # accessing self.field_instance.prefix

    def value_omitted_from_data(self, data, files, name):
        '''
        Given data and files dictionaries and this widget’s name,
        return whether or not there’s data or files for the widget.
        '''
        pass

    # No need to override render(), just put everything in
    # get_context, and set appropriate template
    def get_context(self, name, value, attrs):
        context = super(FormsetWidget, self).get_context(name, value, attrs)
        context['formset'] = value
        return context