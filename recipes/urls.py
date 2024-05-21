from django.urls import path
from . import views
app_name = 'recipes'


urlpatterns = [
    path(
         '',
         views.RecipeListViewHome.as_view(),
         name="home"),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name="search"),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name="category"),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name="recipe"),
    path(
        'recipes/api/v1',
        views.RecipeListViewHomeApi.as_view(),
        name="recipe_api_v1"),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipe_api_v1_detail"),
    path(
        'recipes/tags/<slug:slug>/',
        views.RecipeListViewTag.as_view(),
        name="tag"),
    path(
        'recipes/api/v2/',
        views.RecipeAPIv2ViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name="recipe_api_v2"),
    path(
        'recipes/api/v2/<int:pk>/',
        views.RecipeAPIv2ViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name="recipe_api_v2_detail"),
    path(
        'recipes/api/tag/<int:pk>/',
        views.tag_recipe_api_detail,
        name="recipe_api_v2_tag"),
]
