import json

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, ThreadForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from .models import Posts, ThreadModel, MessageModel, Notification
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Comments, Message
from .forms import CommentForm, MessageForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.core.serializers import serialize



#The @login_required decorater is from django and makes it so that a user must be logged in to see that specific view/page.





'''
Base HTML page for Navbar and footer
'''
def base(request):
    notifications_head = Notification.objects.filter(to_user=request.user).exlcude(is_seen = True)


    return render(request, 'app/base.html', {'notifications_head':notifications_head})

def home(request):
    return render(request, 'app/home.html')

'''
Page for creating an account on the site.
'''
def register(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login')

    else:
        form = RegisterForm()

    return render(request, 'app/register.html', context={'form':form})

@login_required(login_url='/login')
def profile_list(request):
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'app/profile_list.html', {'profiles':profiles, 'notifications':notifications})


def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    try:

        posts = Posts.objects.get(pk=pk)
        notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    except:
        notifications = None
        pass
    #Follow Unfollow Function

    try:

        if request.method == 'POST':
            current_user_profile = request.user.profile
            data = request.POST
            action = data.get('follow')
            like = data.get('')
            if action == 'follow':
                current_user_profile.follows.add(profile)
                new_notification = Notification(action=3, to_user=profile.user, from_user=request.user)  # THIS WILL CREATE A NEW NOTIFCATION OBJECT IN THE NOTIFICAITON MODEL
                new_notification.save()
            elif action == 'unfollow':
                current_user_profile.follows.remove(profile)

            current_user_profile.save()
    except:
        return redirect('/login')

    return render(request, 'app/profile.html', {'profile':profile, 'notifications':notifications})


'''
Page to view the list of followers a user has
'''
def followers(request, pk):
    profile = Profile.objects.get(pk=pk)
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)

    return render(request, 'app/followers.html', {'profile':profile, 'notifications':notifications})


'''
Page to view the list of people a user follows
'''
def following(request, pk):
    profile = Profile.objects.get(pk=pk)
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)

    return render(request, 'app/following.html', {'profile':profile, 'notifications':notifications})

'''
Like a users post
'''
@login_required(login_url='/login')
def LikeView(request, pk):
    post = get_object_or_404(Posts, id=request.POST.get('post_id'))
    post.likes.add(request.user)



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





'''
Remove a like from a post
'''
@login_required(login_url='/login')
def RemoveLike(request, pk):
    post = get_object_or_404(Posts, id=request.POST.get('post_id'))
    post.likes.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def Like(request):
    if request.method == 'POST':
        post = request.POST['post']

        focused_post = Posts.objects.get(id=post)

        if Posts.objects.filter(id=post, likes=request.user).exists():
            focused_post.likes.remove(request.user)
            focused_post.save()


        else:
            focused_post.likes.add(request.user)
            focused_post.save()
            new_notification = Notification(action=1, to_user=focused_post.user, from_user=request.user, post=focused_post) #THIS WILL CREATE A NEW NOTIFCATION OBJECT IN THE NOTIFICAITON MODEL
            new_notification.save()
        success = len(focused_post.likes.all())

        return HttpResponse(success)






'''
Add like to a comment
'''
@login_required(login_url='/login')
def CommentLikeView(request, pk):
    comment = get_object_or_404(Comments, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def CommentLike(request):
    if request.method == 'POST':
        comment = request.POST['comment']

        focused_comment = Comments.objects.get(id=comment)

        if Comments.objects.filter(id=comment, likes=request.user).exists():
            focused_comment.likes.remove(request.user)
            focused_comment.save()

        else:
            focused_comment.likes.add(request.user)
            focused_comment.save()
            like_noti = Notification(action=2, to_user=focused_comment.commenter, from_user=request.user, comment=focused_comment)
            like_noti.save()

        success = len(focused_comment.likes.all())

        return HttpResponse(success)


'''
Remove a like from a comment
'''
@login_required(login_url='/login')
def CommentRemoveLikeView(request, pk):
    comment = get_object_or_404(Comments, id=request.POST.get('comment_id'))
    comment.likes.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



'''
View for /myprofile this shows the user thats logged in their profile
'''
@login_required(login_url='/login')
def my_profile(request):
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    user = request.user
    profile = Profile.objects.get(user=user) #This makes it so that we only grab the stuff for the user logged in
    return render(request, 'app/myprofile.html', {'profile':profile, 'notifications':notifications})




'''
Users can search a specific profile by username
'''

def search_users(request):
    profiles = Profile.objects.all()
    try:
        notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen = True)

    except:
        notifications = None

    if request.method == 'POST':
        profiles = profiles.filter(user__username__contains=request.POST['search_posts'])
    args = {'profiles':profiles, 'notifications':notifications}

    return render(request, 'app/search.html', args)


'''
Feed page for user that is logged in, they can post here and see all posts from users they follow
'''

@login_required(login_url='/login')
def feed(request):
    user = request.user
    profiles = Profile.objects.get(user=user)
    comments = Comments.objects.all()
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/feed')

    else:

        form = PostForm()


    return render(request, 'app/feed.html', {'profiles':profiles, 'form':form, 'comments':comments, 'notifications':notifications})




'''
This is the view where users can view comments on specific posts
'''

def comment_views(request, pk):
    post = Posts.objects.get(id=pk)
    comments = Comments.objects.filter(post=post)
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    new_comment = None
    user = User.objects.get(username=request.user)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.commenter = request.user
            new_comment.save()
            new_notification = Notification(action=4, to_user=post.user, from_user=request.user, post=post) #For notification
            new_notification.save()
            return JsonResponse({'msg': new_comment.comment_content, 'commenter':user.username})
    return render(request, 'app/comment_detail.html', {'post': post, 'comments':comments,'form':form, 'new_comment': new_comment, 'notifications':notifications})

















'''
View posts a user liked!
'''
def view_liked(request, pk):
    profile = Profile.objects.get(pk=pk)
    user = profile.user.id
    posts = Posts.objects.filter(likes=user)
    try:

        notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    except:
        notifications = None


    return render(request, 'app/liked_posts.html', {'profile':profile, 'posts':posts, 'notifications':notifications})



'''
This is the view for just showing all of the conversations/threads a user has.
'''
@login_required(login_url='/login')
def conversation_view(request):
    threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user)) #Grab the thread where the current user is either in user, or receiver field.
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)


    return render(request, 'app/message_view.html', {'threads':threads, 'notifications':notifications})




'''
View for creating a new conversation/thread with a user
'''
@login_required(login_url='/login')
def CreateThread(request):
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        '''
        Check to see if the conversation/thread already exists between the users.. if it does no need to create a new one.
        '''
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver):
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect(f'/specific_thread/{thread.pk}', pk=thread.pk)

            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect(f'/specific_thread'/{thread.pk}, pk=thread.pk)


            '''
            If there is not an existing conversation between the two users then we can go ahead and create a new thread/conversation
            '''
            if form.is_valid():
                thread = ThreadModel(user=request.user, receiver=receiver)
                pk = thread.pk
                thread.save() #Save the thread/conversation to the database.

                return redirect('/create_thread', pk=thread.pk)

        except:
            return redirect('/create_thread')

    else:
        form = ThreadForm()
    return render(request, 'app/create_thread.html', {'form':form, 'notifications':notifications})


'''
View for looking at a specific thread/conversation
'''
@login_required(login_url='/login')
def specific_thread(request, pk):
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)
    verify_thread = ThreadModel.objects.get(pk=pk)
    messages = MessageModel.objects.filter(thread=pk) #Grab all the messages in the specific thread
    form = MessageForm(request.POST)






    if request.method == 'POST':
        thread = ThreadModel.objects.get(pk=pk) #Grab the specific thread
        if thread.receiver == request.user: #Check to see if the the thread receiver is the current logged in user
            receiver = thread.user
        else:
            receiver = thread.receiver
        #If the text box is left blank after hitting send then we are just going to redirect the user back to the page and not create a blank post
        if request.POST.get('message') == '':
            return redirect(f'/specific_thread/{pk}')

        new_message = MessageModel(thread=thread, sender_user=request.user, receiver_user=receiver, body=request.POST.get('message'))
        new_message.save()
        dm_noti = Notification(action=5, to_user=receiver, from_user=request.user)
        dm_noti.save()

        return redirect(f'/specific_thread/{pk}')

    return render(request, 'app/specific_thread.html', {'messages':messages, 'form':form, 'verify_thread':verify_thread, 'notifications':notifications})



'''
View for all notifications for the logged in user!
'''
def notifications(request):
    notifications = Notification.objects.filter(to_user=request.user).exclude(is_seen=True)




    return render(request, 'app/notifications.html', {'notifications':notifications})


'''
When a notification is dismissed it will set its is_seen value to True, therefore the notification wont show in notifications anymore.
'''
def NotificationSeen(request, pk):
    selected_noti = Notification.objects.get(id=pk)
    selected_noti.is_seen = True
    selected_noti.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))









