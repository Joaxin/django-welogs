from django import forms
from markdownx.fields import MarkdownxFormField

# class EmailQuoteForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     email = forms.EmailField()
#     to = forms.EmailField()
#     comments = forms.CharField(required=False, widget=forms.Textarea)

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('name', 'email', 'body')
    
# class SearchForm(forms.Form):
#     query = forms.CharField()

class BlogContentForm(forms.Form):
    content = MarkdownxFormField()
    image = forms.FileField(required=False)