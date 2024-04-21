import os


from django.views.generic import ListView
from recipes.models import Recipe
from utils.pagination import make_pagination


PER_PAGE = int(os.environ.get('PER_PAGE', 9))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_publish=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, 
            context.get('recipes'),
            PER_PAGE
            )

        context.update({
             'recipes': page_obj,
             'pages': pagination_range}
             )
        return context
