import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from taggit.models import Tag

from pokemon.models import Type

from .forms import ArticleForm
from .models import Article, ArticleEdit
from .search_forms import ArticleSearchForm


log = logging.getLogger(__name__)


class WikiHomeView(TemplateView):
    template_name = 'wiki/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WikiHomeView, self).get_context_data(*args, **kwargs)
        context['recent'] = Article.objects.visible_to(self.request.user).order_by('-updated_at')[:5]
        context['articles'] = Article.objects.visible_to(self.request.user).count()
        context['editors'] = ArticleEdit.objects.values('editor').distinct().count()
        return context


class WikiArticleView(TemplateView):
    template_name = 'wiki/article/view.html'
    model = Article

    def get_context_data(self, slug, *args, **kwargs):
        context = super(WikiArticleView, self).get_context_data(*args, **kwargs)
        try:
            context['article'] = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            self.template_name = 'wiki/article-404.html'
            context['title'] = slug.replace('-', ' ').title()
        if context['article'].pokemon:
            context['types'] = Type.objects.all()
        return context


class WikiArticlePublishView(View):

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs.get('pk'))
        article.status = Article.PUBLISHED
        article.save()
        log.debug(article.status)
        return redirect(article.url)


class WikiArticleUnpublishView(View):

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs.get('pk'))
        article.status = Article.DRAFT
        article.save()
        return redirect(article.url)


class WikiEditMixin(object):
    template_name = 'wiki/article/edit.html'
    model = Article
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('wiki.editor'):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'You don\'t have permission to do that')
        return redirect('wiki-index')

    def form_valid(self, form):
        article = form.save(commit=False)
        if not article.id:
            article.author = self.request.user
        article.save()
        form.save_m2m()
        if article.pokemon:
            poke = article.pokemon
            article.tags.add(poke.primary_type.name.title())
            if poke.secondary_type:
                article.tags.add(poke.secondary_type.name.title())
            for cup in poke.cups:
                article.tags.add(cup.name)
        return redirect(self.get_success_url(article))

    def get_success_url(self, article):
        messages.success(self.request, self.message)
        ArticleEdit.objects.create(
            editor=self.request.user,
            article=article
        )
        return reverse('wiki-article', kwargs={'slug': article.slug})


class WikiArticleCreateView(WikiEditMixin, CreateView):
    message = 'Article successfully created!'


class WikiArticleEditView(WikiEditMixin, UpdateView):
    message = 'Article successfully updated!'


class WikiSearchView(SearchView):
    template_name = 'wiki/search.html'
    form_class = ArticleSearchForm
    queryset = SearchQuerySet().order_by('-updated_at')

    def get_context_data(self, *args, **kwargs):
        context = super(WikiSearchView, self).get_context_data(*args, **kwargs)
        context['search'] = self.request.GET.get('q')
        return context


class WikiTagView(ListView):
    template_name = 'wiki/search.html'
    model = Article
    paginate_by = settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE

    def get_context_data(self, *args, **kwargs):
        context = super(WikiTagView, self).get_context_data(*args, **kwargs)
        context['tag'] = self.tag
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(WikiTagView, self).get_queryset(*args, **kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return queryset.filter(tags__name__in=[self.tag.name])
