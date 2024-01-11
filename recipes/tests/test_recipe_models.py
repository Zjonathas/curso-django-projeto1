from .test_recipe_base import RecipeTesteBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTesteBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
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
