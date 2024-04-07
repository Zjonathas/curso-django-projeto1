import os

from django.http.response import Http404
from django.db.models import Q
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.pagination import make_pagination
from django.contrib import messages

from recipes.models import Recipe


PER_PAGE = int(os.environ.get('PER_PAGE', 9))


def home(request):
    recipes = Recipe.objects.filter(is_publish=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    messages.error(request, 'Epa, você foi pesquisar algo que eu vi.')
    messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')
    messages.info(request, 'Epa, você foi pesquisar algo que eu vi.')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pages': pagination_range,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_publish=True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pages': pagination_range,
        'title': f'{recipes[0].category.name} - Category',
    })


def recipe(request, id):    
    recipe = get_object_or_404(Recipe, pk=id, is_publish=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
        Q(title__icontains=search_term) | 
        Q(description__icontains=search_term)),
        is_publish=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search results for "{search_term}" | ',
        'search_term': search_term,
        'recipes': page_obj,
        'pages': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
