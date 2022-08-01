import random
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL  # maps to auth.User


class ArticleQuerySet(models.QuerySet):

    def search(self, query=None):
        if query is None or query == "":
            return self.none()  # Article.objects.none() --- []
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter().filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, null=True, blank=True)

    objects = ArticleManager()

    def get_absolute_url(self):
        # return f'/articles/{self.slug}/'
        return reverse("article-detail", kwargs={"slug": self.slug})

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
