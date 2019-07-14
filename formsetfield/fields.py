""" Created by Oleksandr Sorocynskyi """
""" On 26/05/2019 """

'''
Expected usage in a form:

IngredientsFormset <- modelformset_factory(...)

class RecipeForm(ModelForm):
    ingredients = FormsetForm(formset= IngredeintsFormset)
    
    class Meta:
        ...

class RecipeCreateView(View):
    template_name = '...'

    def get(self, request):
        recipe_form = RecipeForm()

        return render(request,
                      self.template_name,
                      { 'form' : recipe_form, ...})

    def post(self, request):
        recipe_form = RecipeForm(data= request.POST)

        if recipe_form.is_valid():
            recipe_form.create()
            return HttpResponseRedirect(...)
        else:
            return render(request,
                          self.template_name,
                          { 'form' : recipe_form, ...})
    
class RecipeEdit(View):
    template_name = '...'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_form = RecipeCompleteForm(instance= recipe)

        return render(request,
            self.template_name,
            {'form' : recipe_form, ...})

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        form = RecipeCompleteForm(data= request.POST,
                                  files= request.FILES,
                                  instance= recipe)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(...)
        else:
            return render(request,
                          self.template_name,
                          {'form'  : recipe_form,...})


Functions needing implementation:
__init__(data, files, instance)
is_valid
create
save
rendering

Plus make sure it gets initalized by the enclosing form, and all of the above
functions get called when they're called on the enclosing form.


form gets value form formfield.widget
'''

from django.forms.fields import Field

from .widgets import FormsetWidget

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
    This is done in the FOrmsetFIeldFormMixin, hence
    the requirement to be in a form derving form it.
    """
    widget_class = FormsetWidget
    prefix = "formset_field"

    def __init__(self, *, formset_class, **kwargs):
        # Ignore 'initial' argument
        kwargs.pop('initial', None)
        # Instantiate the widget, passing it 'self'
        # so that it can retrieve an update prefix
        widget = self.widget_class(field_instance=self)
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
        return self.formset_class(prefix=self.prefix)
    
    @initial.setter
    def initial(self, val):
        '''
        Set 'initial' property.
        Ignores input value, since intial has to be an instance of a specific
        formset class.
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