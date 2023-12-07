from django.urls import path
from recipes.views import sobre, contato, home

urlpatterns = [
    path('sobre/', sobre),
    path('contato/', contato),
    path('', home),
]