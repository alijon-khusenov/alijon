from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article, Comment
from . import forms
from django.db.models import Q


@login_required(login_url='/users/sign_in')
def home(request):
    search = request.GET.get('search')
    articles = Article.objects.all().order_by('date')
    articles = articles.filter(Q(title__icontains=search) | Q(text__icontains=search)) if search else articles
    return render(request, 'home.html', {'articles': articles})


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.article = article
            instance.save()
            return redirect('articles:article_detail', slug=slug)
    else:
        form = forms.CommentForm()
    return render(request, 'article_detail.html', {'article': article, 'form': form})


def create_article(request):
    if request.method == 'POST':
        form = forms.ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:article_list')
    form = forms.ArticleForm()
    return render(request, 'create_article.html', {'form': form})


def edit_article(request, slug):
    article = Article.objects.get(slug=slug)
    form = forms.ArticleForm(request.POST or None,
                             request.FILES or None, instance=article)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('articles:article_detail', slug=request.POST.get('slug'))
    return render(request, 'edit_article.html', {'form': form, 'article': article})


def delete_article(request, slug):
    article = Article.objects.get(slug=slug)

    if request.method == 'POST':
        article.delete()
        return redirect('articles:article_detail', slug=slug)
    return render(request, 'delete_comment.html', {'comment': comment})

def edit_comment(request, slug, pk):
    comment = Comment.objects.get(pk=pk)
    form = forms.CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('articles:article_detail', slug=slug)
    return render(request, 'edit_comment.html', {'form': form, 'article': comment.article})
        

def delete_comment(request, slug, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('articles:article_detail', slug=slug)
    return render(request, 'delete_comment.html', {'comment': comment})


def like_article(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user not in article.likes.all():
        article.likes.add(request.user)
        article.dislikes.remove(
            request.user) if request.user in article.dislikes.all() else None
    elif request.user in article.likes.all():
        article.likes.remove(request.user)
    return redirect('articles:article_detail', slug=slug)


def dislike_article(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user not in article.dislikes.all():
        article.dislikes.add(request.user)
        article.likes.remove(
            request.user) if request.user in article.likes.all() else None
    elif request.user in article.dislikes.all():
        article.dislikes.remove(request.user)
    return redirect('articles:article_detail', slug=slug)

