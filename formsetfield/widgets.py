""" Created by Oleksandr Sorocynskyi """
""" On 26/05/2019 """

from django.forms.widgets import Widget

class FormsetWidget(Widget):
    '''
    Displays an entire formset
    '''
    template_name = 'formsetwidget/formset.html'




    # This is where the money is!
    def value_from_datadict(self, data, files, name):
        '''
        Extract value from HTML request data, and files,
        given the widget's name.
        The value in this case is a Django Fieldset.
        Note also that value_from_datadict may be called more
        than once during handling of form data, so if you customize it
        and add expensive processing, you should implement some caching mechanism yourself.
        '''
        pass

    def value_omitted_from_data(self, data, files, name):
        '''
        Given data and files dictionaries and this widget’s name,
        returns whether or not there’s data or files for the widget.
        '''
        pass

    # No need to override render(), just put everything in
    # get_context, and set appropriate template
    def get_context(self, name, value, attrs):
        context = super(FormsetWidget, self).get_context(name, value, attrs)
        context['formset'] = value
        return context

    # I think we need to override this since we have multiple HTML tags
    def id_for_label(self, id_):
        return "formset_widget"
