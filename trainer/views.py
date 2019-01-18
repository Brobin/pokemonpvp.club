from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Case, When, Q, F, FloatField, Value
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import TrainerForm
from .mixins import LoginMixin
from .models import Trainer


class TrainerCreate(LoginMixin, CreateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'trainer/edit.html'

    def dispatch(self, *args, **kwargs):
        if hasattr(self.request.user, 'trainer'):
            return redirect(self.request.user.trainer.url)
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        trainer = form.save(commit=False)
        trainer.user = self.request.user
        trainer.save()
        return redirect(trainer.url)


class TrainerEdit(LoginMixin, UpdateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'trainer/edit.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            messages.warning(request, 'You don\'t have permission to edit this!')
            return redirect('trainer-list')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Trainer, name__iexact=self.kwargs['name'])


class TrainerDetail(LoginMixin, DetailView):
    model = Trainer
    template_name = 'trainer/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        trainers = Trainer.objects.count()
        t = context['object']
        # Get all the percentiles for the radar chart
        context['xp'] = Trainer.objects.filter(xp__lte=t.xp).count() / trainers
        context['km'] = Trainer.objects.filter(jogger__lte=t.jogger).count() / trainers
        context['pc'] = Trainer.objects.filter(collector__lte=t.collector).count() / trainers
        context['eh'] = Trainer.objects.filter(breeder__lte=t.breeder).count() / trainers
        context['gl'] = Trainer.objects.filter(great_veteran__lte=t.great_veteran).count() / trainers
        context['ul'] = Trainer.objects.filter(ultra_veteran__lte=t.ultra_veteran).count() / trainers
        context['ml'] = Trainer.objects.filter(master_veteran__lte=t.master_veteran).count() / trainers
        return context

    def get_object(self):
        return get_object_or_404(Trainer, name__iexact=self.kwargs['name'])


class TrainerList(LoginMixin, ListView):
    queryset = Trainer.objects.order_by('-xp')
    template_name = 'trainer/list.html'
    paginate_by = 50
    orderings = [
        ('-xp', 'XP'),
        ('-collector', 'Pokemon Caught'),
        ('-breeder', 'Eggs Hatched'),
        ('-jogger', 'Kilometers Walked'),
        ('-great_veteran', 'Great League Wins'),
        ('-ultra_veteran', 'Ultra League Wins'),
        ('-master_veteran', 'Master League Wins'),
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['orderings'] = self.orderings
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-xp')
        if ordering not in [o[0] for o in self.orderings]:
            return ['-xp']
        return [ordering, '-xp']
