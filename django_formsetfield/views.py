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

from .forms import TestFormsetForm, TestNestedFormsetForm, TestRecipeForm
from .models import Recipe

class TestView(View):
    template_name = 'testform.html'

    def get(self, request):
        #form = TestNestedFormsetForm()

        #form = TestRecipeForm()

        r = Recipe.objects.all()[0]
        form = TestRecipeForm(instance=r)

        return render(request,
                      self.template_name,
                      { 'form' : form })

    def post(self, request):
        #form = TestNestedFormsetForm(request.POST, request.FILES)

        #form = TestRecipeForm(request.POST, request.FILES)

        r = Recipe.objects.all()[0]
        form = TestRecipeForm(data=request.POST, files=request.FILES, instance=r)


        if form.is_valid():
            form.save(commit=True)
            return render(request, "sucess.html")
        else:
            return render(request,
                          self.template_name,
                          { 'form' : form })