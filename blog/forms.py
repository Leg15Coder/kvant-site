from contextlib import nullcontext
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from .models import *

class PostCreateForm(forms.ModelForm):
    all_images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)
    all_documents = forms.FileField(label=u'Документы', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)
    class Meta:
        model = Post
        fields = ('title', 'body', 'status', 'url', 'groups')
        widgets = {'author': forms.HiddenInput(), 'type': forms.HiddenInput()}
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        return post

    '''def clean(self):
        cleaned_data = super(PostCreateForm, self).clean()
        type = cleaned_data.get('type')
        if type=='task':
            PostCreateForm.Meta.fields += 'groups' '''

class RegisterUserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(), label='Пароль:')
    confirm_password=forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль:')
    email = forms.EmailField(max_length=200, label='Почта:')

    class Meta:
        model = User
        fields =  ('username', 'email', 'first_name', 'last_name', 'password')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

class UserActivationForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),
                      'cod-no':
                          ("Код не совпадает."),}


    def __init__(self, *args, **kwargs):
        super(UserActivationForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения', widget=forms.PasswordInput(attrs={'class': 'form-control'}),  error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 50'})



    def save(self, commit=True):
        profile = super(UserActivationForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}

class ChatCreateForm(forms.ModelForm):
    #members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Chat
        fields = ('members', 'name',)
    
    def save(self, commit=True):
        chat = super().save(commit=False)
        if commit:
            chat.save()
        return chat

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = StudentGroups
        fields = ('name', 'teachers', 'type',)
        widgets = {'students': forms.HiddenInput(),}
    
    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        return group

UnactiveProfileCreationForm = modelformset_factory(UnactiveProfile, 
    fields =('surname', 'name', 'patronymic', 'birth_date', 'code'))

'''class UnactiveProfileCreationForm(forms.ModelForm):
    find_code = forms.CharField(required=False)
    class Meta:
        model = UnactiveProfile
        
        widgets = {'user': forms.HiddenInput(), 'code': forms.HiddenInput(),}
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile'''

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields =('body',)
        widgets = {'author': forms.HiddenInput(), 'post': forms.HiddenInput(),}

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        return group