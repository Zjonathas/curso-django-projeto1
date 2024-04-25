import string
from random import SystemRandom
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Here start the fields for the generics relationships'
    # Represents the model we want to place here
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Represents the line id of the model described above
    object_id = models.CharField(max_length=255)
    # A field that represents the generic relationship 
    # that knows the above fields
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
