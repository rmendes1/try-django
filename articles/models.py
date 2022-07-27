import random
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False,
                               null=True,
                               blank=True)

    def get_absolute_url(self):
        return f'/articles/{self.slug}/'

    # Overriding save method
    def save(self, *args, **kwargs):
        # obj = Article.objects.get(id=1)
        # set something
        # if self.slug is None:
        #     slugify_instance_title(self, save=False)
        super().save(*args, **kwargs)
        # obj.save()
        # do another something


def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug=slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        rand_int = random.randint(300_000, 500_000)  # random characters need to be inserted
        slug = f'{slug}-{rand_int}'
        return slugify_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


post_save.connect(article_post_save, sender=Article)
