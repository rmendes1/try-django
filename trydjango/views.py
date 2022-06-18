"""
To render html web pages
"""
from articles.models import Article
from django.shortcuts import render

def home_view(request, id=None, *args, **kwargs):
    """
    Take in a request 
    Return HTML as a response
    """

    article_queryset = Article.objects.all()
    article_obj = Article.objects.get(id=2)
  
    context = {
        "article": article_obj,
        "object_queryset": article_queryset
    }
    
    return render(request=request, template_name="home-view.html", context=context)