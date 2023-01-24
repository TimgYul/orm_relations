from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Scope, Tag

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        check_list = []
        for form in self.forms:
            if len(form.cleaned_data) > 0:
                check_list.append(form.cleaned_data['is_main'])
        if check_list.count(True) > 1:
            raise ValidationError('Основным может один раздел')
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            # form.cleaned_data
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if check_list.count(True) == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода
    
class RelationshipInline(admin.TabularInline):
    model = Scope
    extra = 2
    formset = RelationshipInlineFormset

    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list = ['id', 'name']
    
