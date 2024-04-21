import os

from django.http.response import Http404
from django.db.models import Q
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.pagination import make_pagination

from recipes.models import Recipe


PER_PAGE = int(os.environ.get('PER_PAGE', 9))


def recipe(request, id):    
    recipe = get_object_or_404(Recipe, pk=id, is_publish=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
