from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(PostImages)
admin.site.register(PostDocuments)
admin.site.register(Profile)
admin.site.register(StudentGroups)
admin.site.register(Comments)
admin.site.register(Reaction)
admin.site.register(AnswerToTask)
admin.site.register(UnactiveProfile)