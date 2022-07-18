from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False,
                               null=True,
                               blank=True)

    # Overriding save method
    def save(self, *args, **kwargs):
        # obj = Article.objects.get(id=1)
        # set something
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # obj.save()
        # do another something
