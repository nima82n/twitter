
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post', views.post_related_tasks, name='new_post'),
    path('profile/<int:userId>', views.profile, name='profile'),
    path('following', views.following_page, name='following'),
    # API Routes
    path('profile/follow_unfollow', views.FollowUnfollow.as_view(), name='follow_unfollow'),
    path('edit', views.post_related_tasks, name='edit'),
    path('likeunlike', views.post_related_tasks, name='like'),
    path('likeNum/<int:pk>', views.post_related_tasks, name='likeNum'),
]