from tkinter import CASCADE
from unicodedata import name
from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

class PublishedManager(models.Manager):  
    def get_queryset(self):  
        return super(PublishedManager, self).get_queryset().filter(status='published')

class UnactiveProfile(models.Model):
    code = models.CharField(max_length=16, blank=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40)
    birth_date = models.DateTimeField(auto_now=False) 

class StudentGroups(models.Model):
    name = models.CharField(max_length=9) 
    students = models.ManyToManyField(UnactiveProfile, related_name="Ученики")
    teachers = models.ManyToManyField(User, related_name="Наставники")
    type = models.CharField(max_length=20) 

    def get_absolute_url(self):  
        return reverse('blog:group_detail', args=[self.id,]) 

class Post(models.Model): 
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'), ) 
    TYPE_CHOICES = (('task', 'Task'), ('news', 'News'), ('post', 'Post'), ('forum', 'Forum'), )
    
    title = models.CharField(max_length=150) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') 
    body = models.TextField() 
    publish = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published') 
    objects = models.Manager()  
    published = PublishedManager() 
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='post')
    groups = models.ManyToManyField(StudentGroups, verbose_name="Группы", null=True, blank=True)
    url = models.URLField(verbose_name="ССылки на видео", null=True, blank=True)
    #tags = ArrayField(models.CharField(max_length=30, blank=True, null=True), size=10, null=True, blank=True)

    def get_absolute_url(self):  
        return reverse('blog:post_detail', args=[self.id,]) 

    class Meta: 
        ordering = ('-publish',) 

    def __str__(self): 
        return self.title

class PostImages(models.Model):
    image_data_link = models.ImageField(upload_to='images/posts/%Y/%m/%d/')
    image_url = models.URLField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='all_images')

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def get_remote_url(self):
        if self.image_url and not self.image_data_link:
            image_temp = NamedTemporaryFile(delete=True)
            image_temp.write(requests.get(self.image_url).content)
            image_temp.flush()
            self.image_data_link.save(f'photo_{self.pk}.jpg', File(image_temp))
        self.save()

class PostDocuments(models.Model):
    document_data_link = models.FileField(upload_to='documents/posts/%Y/%m/%d/')
    document_url = models.URLField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='all_documents')

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def get_remote_url(self):
        if self.document_url and not self.document_data_link:
            document_temp = NamedTemporaryFile(delete=True)
            document_temp.write(requests.get(self.document_url).content)
            document_temp.flush()
            self.document_data_link.save(f'photo_{self.pk}.jpg', File(document_temp))
        self.save()

class Profile(models.Model):
    CHOICES = (('guest', 'Guest'), ('student', 'Student'), ('teacher', 'Teacher'), ('worker', 'Worker'), ('none', 'None'), ('manage', 'Manage'), ('graduate', 'Graduate'),) 

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='images/icons/', blank=True, null=True, default='static\img\icon.ico')
    status = models.CharField(max_length=90, null=True, blank=True) 
    type = models.CharField(max_length=15, choices=CHOICES, default='none') 
    groups = models.ManyToManyField(StudentGroups, related_name="Группы", null=True, blank=True)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(owner=instance)

    post_save.connect(create_user_profile, sender=User)

class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, ('Dialog')),
        (CHAT, ('Chat'))
    )
 
    type = models.CharField(
        ('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=("Участники"))
    name = models.CharField(max_length=20, default='')

    #@models.permalink
    def get_absolute_url(self):
        return self.pk
 
class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(("Сообщение"))
    pub_date = models.DateTimeField(('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(('Прочитано'), default=False)
 
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message

class Comments(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=("Пользователь"), on_delete=models.CASCADE)
    pub_date = models.DateTimeField(('Дата'), default=timezone.now)
    body = models.TextField()

    class Meta:
        ordering=['pub_date']

class Reaction(models.Model):
    name = models.CharField(max_length=64)
    icon = models.ImageField()
    number = models.IntegerField()
    target = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)

class AnswerToTask(models.Model): 
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'), ) 
    
    student = models.ForeignKey(User, on_delete=models.CASCADE) 
    body = models.TextField() 
    publish = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published') 
    task = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_absolute_url(self):  
        return reverse('blog:post_detail', args=[self.id,]) 

    class Meta: 
        ordering = ('-publish',) 

    def __str__(self): 
        return self.title