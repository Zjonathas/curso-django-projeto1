from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from ..serializers import TagSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 10


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_publish()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


@api_view()
def tag_recipe_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False,
                               context={'request': request})
    return Response(serializer.data)
