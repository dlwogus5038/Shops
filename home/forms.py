from django import forms
#from .models import ProfileSite

class UserForm(forms.Form):
    username = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Username',
                }
            )
    )
    password = forms.CharField(
            required=True,
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': 'Password',
                }
            )
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(UserForm, self).clean()


class SearchForm(forms.Form):
    LOC = 'LOC'
    FOODTYPE = 'FOODTYPE'
    TASTE = 'TASTE'
    SERVICE = 'SERVICE'
    ENVI = 'ENVI'
    COMMENT = 'COMMENT'
    SEARCH_CHOICES = (
        (LOC, '按区域'),
        (FOODTYPE, '按分类'),
        (COMMENT, '按评论')
    )
    SORT_CHOICES = (
        (TASTE, '按味道'),
        (SERVICE, '按服务'),
        (ENVI, '按环境')
    )
    search_choice = forms.ChoiceField(choices=SEARCH_CHOICES, label='选择搜索方式')
    sort_choice = forms.ChoiceField(choices=SORT_CHOICES, label='选择排序方式')
    search_input = forms.CharField(max_length=1000, label='输入搜索信息')
    # text_input = forms.CharField(max_length=1000, label='输入评论内容', widget=forms.Textarea)


'''class CharForm(forms.Form):
    search_input = forms.CharField(max_length=20, label='输入搜索信息')


class TextForm(forms.Form):
    text_input = forms.CharField(max_length=1000, label='输入评论内容', widget=forms.Textarea)'''





