from unittest.mock import patch
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # User open the page
        self.browser.get(self.live_server_url)

        # See a field from search with text "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Click in this input and type the search term
        # for find the recipe with o title wanted
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(title_needed, 
                      self.browser.find_element(By.CLASS_NAME, 
                                                'main-content-list').text
                      )


    @patch('recipes.views.list_view_recipe.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # User open the page
        self.browser.get(self.live_server_url)

        # See have a pagination and click on page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        self.sleep(0)

        # See there are 2 more recipes
        self.assertEqual(
            len(self.browser.find_elements(
                By.CLASS_NAME,
                'recipe'
            )),
            2
        )
