from django.http.response import Http404
from django.db.models import Q
from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range


def home(request):
    recipes = Recipe.objects.filter(is_publish=True).order_by('-id')

    paginator = Paginator(recipes, 9)

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    pag_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page,
    )

    page = paginator.get_page(1)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page,
        'pages': pagination_range,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_publish=True,
        ).order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
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

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search results for "{search_term}" | ',
        'search_term': search_term,
        'recipes': recipes,
    })
