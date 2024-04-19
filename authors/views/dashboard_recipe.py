from django.views import View
from django.http.response import Http404
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse


class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_publish=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404

        return recipe

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', {
                'form': form,
                }
        )

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_publish = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso.')
            return redirect(reverse(
                'authors:dashboard_recipe_edit',
                args=(recipe.id,)
                )
                )

        return self.render_recipe(form)
