"""
To render html web pages
"""
from articles.models import Article
from django.shortcuts import render

def home_view(request, *args, **kwargs):
    """
    Take in a request 
    Return HTML as a response
    """

    article_queryset = Article.objects.all()
  
    context = {
        "object_queryset": article_queryset
    }
    
    return render(request=request, template_name="home-view.html", context=context)