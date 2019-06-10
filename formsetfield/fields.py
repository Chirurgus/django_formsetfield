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
    Field that can have display an entire formset.
    """
    widget = FormsetWidget
    template_name = "...."

    def __init__(self, *, formset, **kwargs):
        super().__init__(**kwargs)
        if formset is None:
            raise ValueError('formset argument has to be not None.')
        self.initial = formset() if isinstance(formset, type) else formset

    def clean(self, value):
        '''
        Return clean value from the raw value extracted from the widget.
        '''
        pass
  
    def to_python(self, value):
        ''' 
        Return a Django Formset instance.
        '''
        pass


    def get_prefix(self, form, name):
        """
        Return the prefix that is used for the formset.
        """
        return '{form_prefix}{prefix_name}-{field_name}'.format(
            form_prefix=form.prefix + '-' if form.prefix else '',
            prefix_name=self.prefix_name,
            field_name=name)

