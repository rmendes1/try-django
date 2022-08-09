from django.contrib import admin
from .models import RecipeIngredient, Recipe
from django.contrib.auth import get_user_model


User = get_user_model()


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    # fields = ['name', 'quantity', 'unit', 'directions']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']  # makes you search for the field in a separate search window


admin.site.register(Recipe, RecipeAdmin)
