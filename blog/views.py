from django.shortcuts import render, get_object_or_404 
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import *
from django.core.files.base import ContentFile
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def post_list(request, type): 
    object_list = Post.published.filter(type=type, status="published")  
    page = request.GET.get('page')  
    form = PostCreateForm(request.POST, request.FILES)
    profile = Profile.objects.get(owner=request.user)
    paginator = Paginator(object_list, 7)

    if form.is_valid():
        new_obj = form.save(commit=False)
        new_obj.author = request.user
        new_obj.type = type
        new_obj = form.save()
        for image in request.FILES.getlist('all_images'):
            data = image.read() 
            i = PostImages(post=new_obj)
            i.image_data_link.save(image.name, ContentFile(data))
            i.save()
        for doc in request.FILES.getlist('all_documents'):
            data = doc.read() 
            d = PostDocuments(post=new_obj)
            d.document_data_link.save(doc.name, ContentFile(data))
            d.save()
        return redirect(new_obj)
    try:  
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        posts = paginator.page(1)  
    except EmptyPage:  
        posts = paginator.page(paginator.num_pages)  

    context = {
        'page': page, 
        'posts': posts, 
        'form': form,
        'profile': profile,
    }
    return render(request, 'post/list.html', context)

def post_detail(request, id):  
    post = get_object_or_404(Post, status='published', id=id) 
    Images = PostImages.objects.filter(post=post)
    Documents = PostDocuments.objects.filter(post=post)
    comments = Comments.objects.all().filter(post=post)

    form = CommentsForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment = form.save()
        comment.save()

    context = {
        'post': post, 
        'Images': Images, 
        'Documents': Documents,
        'commentform': form,
        'comments': comments,
        }
    return render(request, 'post/detail.html', context)

def home(request):
    context = {}
    template = 'descr.html'
    return render(request, template, context)

def generate_code(type):
    if type=='email':
        random.seed()
        return str(random.randint(100000,999999))
    elif type=='student':
        random.seed()
        code = str(hex(random.randint(1,54240)))
        while UnactiveProfile.objects.filter(code=code)!=None:
            code = str(hex(random.randint(1,813615)))
        return code


def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegisterUserForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password')
                u_f = User.objects.get(username=username, email=email)
                code = generate_code('email')
                if Profile.objects.filter(code=code):
                    code = generate_code('email')

                user = authenticate(username=username, password=my_password1)
                profile = Profile.objects.get(owner=u_f)
                profile.code = code
                profile.save()
                html_message = render_to_string('account/active_message.html', {'code': code})
                plain_message = strip_tags(html_message)

                send_mail('Подтверждение аккаунта',plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)

                if user and user.is_active:
                    login(request, user)
                    return redirect('home')
                else: #тут добавить редирект на страницу с формой для ввода кода.
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('/activation_code_form/')
            else:
                return render(request, 'account/register.html', {'form': form})
        else:
            return render(request, 'account/register.html', {'form':
            RegisterUserForm()})
    else:
        return redirect('home')

def endreg(request):
    if  request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserActivationForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if Profile.objects.filter(code=code_use):
                    profile = Profile.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'account/user_activation.html', {'form': form})
                if profile.owner.is_active == False:
                    profile.owner.is_active = True
                    profile.owner.save()
                    login(request, profile.owner)
                    return redirect('home')
                else:
                    form.add_error(None, '1Unknown or disabled account')
                    return render(request, 'account/user_activation.html', {'form': form})
            else:
                return render(request, 'account/user_activation.html', {'form': form})
        else:
            form = UserActivationForm()
            return render(request, 'account/user_activation.html', {'form': form})

class LoginUserView(LoginView):
    template_name = 'account/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('post_list')
    def get_sucess_url(self):
        return self.success_url

class LogoutSys(LogoutView):
    next_page = reverse_lazy('home')

def profile_user_view(request, user):
    owner = User.objects.get(username=user)
    profile = Profile.objects.get(owner=owner)
    context = {'profile': profile,}
    template = 'account/profile.html'
    return render(request, template, context)

class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.all().filter(members__in=[request.user.id])
        context = {
            'user_profile': request.user, 
            'chats': chats,
            'form': ChatCreateForm,
        }
        return render(request, 'message/list.html', context)

    def post(self, request):
        form = ChatCreateForm(data=request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat = form.save()
            chat_id = chat.id
            MembersCount = form.cleaned_data.get("members").count()
            if MembersCount==2:
                chat.type = 'D'
            else:
                chat.type = 'C' 
            for u in form.cleaned_data.get("members"):
                chat.members.add(u)
            if request.user not in chat.membres:
                chat.members.add(request.user)
            chat.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))

class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        context = { 
            'user_profile': request.user,
            'chat': chat,
            'form': MessageForm()
            }

        return render(request,'message/room.html',context)
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))

def info(request, type='all'):
    if type=='all':
        context = {}
        template = 'descr.html'
        return render(request, template, context)
    elif type=='promrobo':
        context = {}
        template = 'info/promrobo.html'
    elif type=='it':
        context = {}
        template = 'info/it.html'
    elif type=='vr':
        context = {}
        template = 'info/vr.html'
    elif type=='promdesign':
        context = {}
        template = 'info/promdesign.html'
    elif type=='geo':
        context = {}
        template = 'info/geo.html'
    elif type=='haiteg':
        context = {}
        template = 'info/haiteg.html'
    elif type=='imedia':
        context = {}
        template = 'info/imedia.html'
    return render(request, template, context)

class GroupsView(View):
    def get(self, request):
        groups = StudentGroups.objects.all().filter(teachers__in=[request.user.id])
        context = {
            'groups': groups,
        }
        return render(request, 'gradation/list.html', context)

    def post(self, request):
        form = GroupCreateForm
        if form.is_valid():
            group = form.save(commit=False)
            group = form.save()
            group.teachers.add(request.user)
            group.save()
            group_id = group.id
        return redirect(reverse('group_detail', kwargs={'group_id': group_id}))

class CreateGroupView(View):
    def get(self, request):
        formset = UnactiveProfileCreationForm(queryset=UnactiveProfile.objects.none())
        return render(request, "gradation/groupscreate.html", {'formset': formset})

    def post(self, request):
        formset = UnactiveProfileCreationForm(data=request.POST)
        form = GroupCreateForm(data=request.POST)

        if form.is_valid() and formset.is_valid():
            f1 = form.save(commit=False)
            f2 = formset.save(commit=False)
            for f in f2:
                stud = UnactiveProfile.objects.filter(name=f.name, surname=f.surname, patronymic=f.patronymic, birth_date=f.birth_date)
                if f.code in [None, '', ' '] and stud==None:
                    stud = Profile.objects.filter(first_name=f.name, username=f.surname, last_name=f.patronymic, birth_date=f.birth_date)
                    if stud!=None:
                        f.code = Profile.objects.get(first_name=f.name, username=f.surname, last_name=f.patronymic, birth_date=f.birth_date).code
                    else:
                        f.code = generate_code('student')
                elif stud!=None:
                    f = UnactiveProfile.objects.get(name=f.name, surname=f.surname, patronymic=f.patronymic, birth_date=f.birth_date) 
                else:
                    f = UnactiveProfile.objects.get(code=f.code)
                    if f==None:
                        f = Profile.objects.get(code=f.code)
                f.save()
                f1.students += f
            formset.save()
            form.save()
            return redirect(reverse_lazy("home"))
        return render(request, "gradation/groupscreate.html", {'formset': formset, 'form': form})

def group_detail(request, id):  
    group = get_object_or_404(StudentGroups, id=id) 
    return render(request, 'gradation/group_detail.html', {'group': group,})