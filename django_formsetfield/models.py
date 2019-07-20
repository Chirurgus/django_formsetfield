# Created by Oleksandr Sorochynskyi
# On 19/07/2019

from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=100, default= "")

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.CharField(max_length=100, null= True, blank= True)


