from django import forms
from .models import Article


class ArticleFormOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        qs = Article.objects.all().filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', f"\"{title}\" is already in use.")
        return data


    # def clean_title(self):
    #     cleaned_data = self.cleaned_data  # dict
    #     print("cleaned data", cleaned_data)
    #     title = cleaned_data.get('title')  # only part of it (cleaned)
    #     if title.lower().strip() == 'the office':
    #         raise forms.ValidationError('This title is already taken.')
    #     print("title", title)
    #     return title

    # def clean(self):
    #     cleaned_data = self.cleaned_data  # all data
    #     title = cleaned_data.get('title')
    #     content = cleaned_data.get('content')
    #     if title.lower().strip() == 'the office':
    #         self.add_error('title', 'This title is already taken.')
    #         #raise forms.ValidationError('This title is already taken.')
    #
    #     if 'office' in content or 'office' in title.lower():
    #         self.add_error('content', "Office cannot be in content")  # add error for only specific sections of the form
    #         raise forms.ValidationError("Office is not allowed")      # valid. error for the whole form
    #     return cleaned_data
