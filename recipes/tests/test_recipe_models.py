from .test_recipe_base import RecipeTesteBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTesteBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category = self.make_category(name='Test Default Category'),
            author = self.make_author(username='Test Default Author'),
            title = 'Recipe Title',
            description = 'Description',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            servings_unit = 'Porções',
            preparation_steps = 'Recipe preparations steps',
        )

        recipe.full_clean()
        recipe.save()

        return recipe
    
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_legth(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_html, 
                         msg= 'Recipe preparation steps html is not False')
    
    def test_recipe_is_publish_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_publish, 
                         msg= 'Recipe is publish is not False')
    
    def test_recipe_string_represatation(self):
        needed = 'Testing Represatation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed,
                         msg=f'Recipe string representation must be' \
                            f'"{needed}" but "{str(self.recipe)}" '\
                                'was received')
