from django.urls import path
from . import views
urlpatterns = [
    path('base', views.base, name='base'),
    path('register', views.register, name='register'),
    path('profile_list', views.profile_list, name='profile_list'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('search', views.search_users, name='search'),
    path('myprofile', views.my_profile, name='my_profile'),
    path('feed', views.feed, name='feed'),
    path('like/<int:pk>', views.LikeView, name='like_post'),
    path('remove_like/<int:pk>', views.RemoveLike, name='removelike_post'),
    path('followers/<int:pk>', views.followers, name='followers'),
    path('following/<int:pk>', views.following, name='following'),
    path('comment_like/<int:pk>', views.CommentLikeView, name='comment_like_post'),
    path('comment_remove_like/<int:pk>', views.CommentRemoveLikeView, name='comment_remove_like_post'),
    path('liked_posts/<int:pk>', views.view_liked, name='view_liked_posts'),
    path('conversations', views.conversation_view, name='conversation'), #List the threads
    path('create_thread', views.CreateThread, name='create_thread'),
    path('specific_thread/<int:pk>', views.specific_thread, name='specific_thread'),
    path('like', views.Like, name='like'),
    path('like_comment', views.CommentLike, name='like_comment'),
    path("notifications", views.notifications, name='notifications'),
    path('comments/<int:pk>', views.comment_views, name='comment_detail'),
    path('delete_noti/<int:pk>', views.NotificationSeen, name='delete_noti'),
]