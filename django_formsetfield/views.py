from django.views import View

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    DeleteView,
    UpdateView,
    CreateView,
)

from .forms import TestFormsetForm, TestNestedFormsetForm

class TestView(View):
    template_name = 'testform.html'

    def get(self, request):
        form = TestNestedFormsetForm()

        return render(request,
                      self.template_name,
                      { 'form' : form })

    def post(self, request):
        form = TestNestedFormsetForm(request.POST, request.FILES)
        
        if form.is_valid():
            return render(request, "sucess.html")
        else:
            render(request,
                    self.template_name,
                    { 'form' : form })

'''
class RecipeCreate(View):
    template_name = 'recipe/edit.html'

    def get(self, request):
        recipe_form = RecipeCompleteForm()

        return render(request,
                      self.template_name,
                      { 'form' : recipe_form,
                        'new'  : True })

    # PUT method is not allowed for HTML forms,
    # so POST is used even for new instances
    def post(self, request):
        recipe_form = RecipeCompleteForm(data= request.POST)

        if recipe_form.is_valid():
            recipe_form.create()
            return HttpResponseRedirect(reverse('recipe-list'))
        else:
            return render(request,
                          self.template_name,
                          { 'form' : recipe_form,
                            'new'  : True  })

class RecipeImport(BaseLoginRequiredMixin, View):
    template_name = 'recipe/import.html'

    submit_button_name = 'import-url'

    def get(self, request):
        return render(request,
                      self.template_name,
                      {'submit_button_name' : self.submit_button_name})

    def post(self, request):
        import_url = request.POST.get(self.submit_button_name, None)
        try:
            recipe = scrape(import_url)
            return HttpResponseRedirect(
                reverse('recipe-edit',
                        kwargs= { 'pk': recipe.id }))

        except WebsiteNotImplementedError:
            return render(request,
                      self.template_name,
                      {'submit_button_name' : self.submit_button_name,
                       'error'              : 'This domain is not supported' })

class RecipeEdit(BaseLoginRequiredMixin, View):
    template_name = 'recipe/edit.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_form = RecipeCompleteForm(instance= recipe)

        return render(request,
            self.template_name,
            {'recipe'    : recipe,
             'form'      : recipe_form})

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        form = RecipeCompleteForm(data= request.POST,
                                  files= request.FILES,
                                  instance= recipe)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('recipe-detail',
                        kwargs= {'pk': pk}))
        else:
            return render(request,
                          self.template_name,
                          {'recipe'  : recipe,
                           'form'    : form })
'''