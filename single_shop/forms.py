from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(label='', max_length=1000, widget=forms.Textarea)