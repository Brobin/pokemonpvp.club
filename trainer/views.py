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

    def get_object(self):
        return get_object_or_404(Trainer, username__iexact=self.kwargs['username'])


class TrainerDetail(LoginMixin, DetailView):
    model = Trainer
    template_name = 'trainer/detail.html'

    def get_object(self):
        return get_object_or_404(Trainer, name__iexact=self.kwargs['name'])


class TrainerList(LoginMixin, ListView):
    queryset = Trainer.objects.order_by('-xp')
    template_name = 'trainer/list.html'
    paginate_by = 50

