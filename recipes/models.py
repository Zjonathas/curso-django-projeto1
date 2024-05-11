from collections import defaultdict
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from tag.models import Tag
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from PIL import Image
from random import SystemRandom
import string


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_publish(self):
        return self.filter(
            is_publish=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id').select_related('category', 'author')\
            .prefetch_related('tags')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165, verbose_name=_('Description'))  # noqa: E501
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name=_('Preparation time'))
    preparation_time_unit = models.CharField(max_length=65, verbose_name=_('Preparation time unit'))  # noqa: E501
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(max_length=65, verbose_name=_('Servings unit'))  # noqa: E501
    preparation_steps = models.TextField(verbose_name=_('Preparation steps'))
    preparation_steps_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=False, verbose_name=_('Is publish'))  # noqa: E501
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')  # noqa: E501
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,  # noqa: E501
                                 default=None,)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=60,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')

        saved = super().save(*args, **kwargs)

        try:
            if self.cover:
                self.resize_image(self.cover, 840)
        except FileNotFoundError:
            ...

        return saved

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
