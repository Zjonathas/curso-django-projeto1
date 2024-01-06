from django.shortcuts import render
from utils.recipe.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404

def home(request):
    recipes = Recipe.objects.filter(is_publish = True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_publish=True
    ).order_by('-id')

    if not recipes:
        raise Http404('Category not found')

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes.firts().category.name} - Category',
    })

def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })