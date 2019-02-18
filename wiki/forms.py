from django import forms

from markdownx.widgets import MarkdownxWidget

from pokemon.models import Pokemon
from .models import Article


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=MarkdownxWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs['class'] = 'form-control'
        self.fields['pokemon'].queryset = Pokemon.objects.order_by('name')

    class Meta:
        model = Article
        fields = ['title', 'content', 'tags', 'pokemon']
