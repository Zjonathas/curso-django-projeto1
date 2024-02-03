from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTesteBase

class RecipeSearchTermTest(RecipeTesteBase):   
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)

        self.assertIs(resolved.func, views.search)
    
    def test_recipe_search_load_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed('recipes/pages/search')
    
    def test_recipe_search_404_if_no_seach_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_term_ison_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<Test>')
        self.assertIn(
            'Search results for &quot;&lt;Test&gt;&quot; | Recipes',
            response.content.decode('utf-8')
        )
