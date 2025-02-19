from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from .models import User, Post, Follow
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404 
from django.http import Http404


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj,
    })


class Login(LoginView):
    template_name = 'network/login.html'
    authentication_form = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('index')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# @api_view(['POST'])
# def new_post(request):
#     print(request.data)
#     user = request.user
#     content = request.POST['content']
#     post = Post(user=user, content=content)
#     post.save()
#     return HttpResponseRedirect(reverse(index))


def profile(request, userId):
    user = User.objects.get(pk=userId)
    viewer = request.user
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    followers = user.followers.all()
    followings = user.followings.all()
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if viewer != user:
        self = False
        
    else:
        self = True
    
    for i in followers:
        if i.user == viewer:
            follows = True
            break
    else:
        follows = False
    
    return render(request, 'network/profile.html', {
        'page_obj': page_obj,
        'followings': followings,
        'followers': followers,
        'self': self,
        'follows': follows,
        'userf': user,
    })


class FollowUnfollow(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You should login first!'})
        user = request.user
        user_to_follow = User.objects.get(pk=int(request.data.get('userId')))
        if Follow.objects.filter(user=user, user_to_follow=user_to_follow).exists():
            return Response({'error': 'You already followed this user.'})
        Follow.objects.create(user=user, user_to_follow=user_to_follow)
        return Response({'message': 'Followed successfully.'})
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You should login first!'})
        user = request.user
        user_to_follow = User.objects.get(pk=int(request.data.get('userId')))
        objs = Follow.objects.filter(user=user, user_to_follow=user_to_follow)
        for obj in objs:
            obj.delete()
        return Response({'message': 'Unfollowed successfully.'})


@login_required
def following_page(request):
    user = request.user
    followings = Follow.objects.filter(user=user).values_list('user_to_follow', flat=True)
    posts = Post.objects.filter(user__in=followings)
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        'page_obj': page_obj,
    })


class Edit(generics.UpdateAPIView):
    serializer_class = PostSerializer
    
    def get_object(self):
        postId = self.request.data.get('postId')
        return Post.objects.get(pk=postId)


# class LikeUnlikeNum(APIView):
#     def put(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return Response({'error': 'login required.'})
#         post = Post.objects.get(pk=request.data.get('postId'))
#         post.likes.add(request.user)
#         return Response({'message': 'liked.'})
    
#     def delete(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return Response({'error': 'login required.'})
#         post = Post.objects.get(pk=request.data.get('postId'))
#         post.likes.remove(request.user)
#         return Response({'message': 'unliked.'})


@api_view(['POST', 'GET', 'PATCH'])
def post_related_tasks(request, pk=None, *args, **kwargs):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'authentication required.'})
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
        return HttpResponseRedirect(reverse(index))
    
    if request.method == 'GET':
        if pk is not None:
            post = get_list_or_404(Post, pk=pk)
            for i in post:
                post = i
            return Response({'likes': post.likes.count()})
        data = PostSerializer(Post.objects.all(), many=True).data
        return Response(data)
    
    if request.method == 'PATCH':
        if not request.user.is_authenticated:
            return Response({'error': 'authentication required.'})
        data = request.data
        action = data.get('action')
        obj = get_list_or_404(Post, pk=data.get('postId'))
        for post in obj:
            if action == 'like':
                post.likes.add(request.user)
                return Response({'messege': 'liked'})
            elif action == 'unlike':
                post.likes.remove(request.user)
                return Response({'messege': 'unliked'})
            elif action == 'edit':
                if post.user == request.user:
                    post.content = data.get('content')
                    post.save()
                    return Response({'messege': 'edited'})
                else:
                    return Response({'error': 'only the author can edit the post.'})