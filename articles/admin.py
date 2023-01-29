from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article,Scope,Tag

class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tag_counter = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_tag_counter += 1
        if main_tag_counter < 1:
            raise ValidationError('Нужно выбрать один Тег. Вы не выбрали ниодного.')
        if main_tag_counter > 1:
            raise ValidationError('Нужно выбрать один Тег. Вы выбрали больше одного.')
        return super().clean()


class ArticleScopeInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = ArticleScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text',  'published_at', 'image']
    inlines = [ArticleScopeInline, ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id','name']
