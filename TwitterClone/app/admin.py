from django.contrib import admin
from .models import Profile
# Register your models here.
from django.contrib.auth.models import User
from .models import Posts
from .models import Comments, Message, MessageModel, ThreadModel, Notification
'''
Merges profiles with Users
'''

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Posts)


admin.site.register(Comments)

admin.site.register(Message)

admin.site.register(ThreadModel)

admin.site.register(MessageModel)

admin.site.register(Notification)
