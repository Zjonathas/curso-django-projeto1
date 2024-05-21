from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from ..serializers import TagSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 10


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_publish()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    # def get(self, request):
    #     recipes = Recipe.objects.get_publish()[:10]
    #     serializer = RecipeSerializer(instance=recipes, many=True,
    #                                   context={'request': request})
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = RecipeSerializer(data=request.data,
    #                                   context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(
    #         author_id=1,
    #         category_id=1,
    #         tags=[1, 2]
    #     )
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_publish()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


@api_view()
def tag_recipe_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False,
                               context={'request': request})
    return Response(serializer.data)
