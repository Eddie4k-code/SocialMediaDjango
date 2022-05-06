from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

'''
Where profiles are stored
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    user_image = models.ImageField(default='../images/default-user.jpg')

    def __str__(self):
        return self.user.username #Allows us to see the username in the /admin under follows


'''
Where user posts are stored
'''
class Posts(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked')

    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return (
            f'{self.user} '
            f'({self.created_at:%Y-%m-%d %H:%M}): '
            f'{self.body[:30]}....'
            f'{self.likes}'
        )





'''
Where comments are stored
'''
class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name = 'comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.CharField(max_length=90)
    comment_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_liked')

    class Meta:
        get_latest_by = ['comment_time']



    def __str__(self):
        return (
            f'{self.post}'
            f'{self.commenter}'
            f'({self.comment_time}'
            f'{self.comment_content}'
            f'{self.likes}'
        )


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='form_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


'''
Models for user threads where a conversationm will be located.
'''
class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class MessageModel(models.Model):
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, related_name='+', blank=True, null=True) #Use this to be able to tell what thread the messages come from
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uplaods/message_photos', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)




class Notification(models.Model):
    action = models.IntegerField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_noti')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_noti')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_noti', null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='comment_noti', null=True, blank=True)
    is_seen = models.BooleanField(default=False)



'''
This allows a user to follow themselves once an account is created...
'''
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()










