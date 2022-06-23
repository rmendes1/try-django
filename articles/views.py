from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Article
from .forms import ArticleForm


def article_detail_view(request, id=None):
    article_obj = None
    
    if id is not None:
        article_obj = Article.objects.get(id=id)

    context = {
        "object": article_obj
    }

    return render(request, "articles/detail.html", context=context)


def article_search_view(request):

    query_dict = request.GET # it is a dict

    try:
        query = int(query_dict.get("q"))

    except:
        query = None
    article_obj = None
    if query is not None:
        article_obj = Article.objects.get(id=query)
    context = {
        "object": article_obj
    }

    return render(request, "articles/search.html", context=context)

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        article_object = form.save()
        context['form'] = ArticleForm()
        #context['object'] = article_object
        #context['created'] = True

    return render(request, "articles/create.html", context=context)
