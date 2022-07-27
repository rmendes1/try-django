from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm


def article_detail_view(request, slug=None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:  # slug does not exist
            raise Http404
        except Article.MultipleObjectsReturned:  # slug is duplicated
            article_obj = Article.objects.filter(slug=slug).first()
        except Exception as e:
            print(e)  # temporary
            raise Http404

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
        return redirect(article_object.get_absolute_url())  # article-detail

    return render(request, "articles/create.html", context=context)
