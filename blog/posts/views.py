from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentForm, PostForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']
        comment = Comment.objects.get(id=comment_id)
        if request.user != comment.author:
            # Возвращаем ошибку или редирект, если пользователь не автор комментария
            return redirect('post_detail', pk=comment.post.pk)
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)


class MyPostsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
        return render(request, 'posts/my_posts.html', {'posts': posts, 'is_homepage': True})


# Create your views here.
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    for post in posts:
        post.is_liked = post.is_liked_by_user(request.user)
    return render(request, 'posts/post_list.html', {'posts': posts, 'form': form, 'is_homepage': True})


def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
        context = {
            'post': post,
            'comment_form': form,
            'is_homepage': False,  # Устанавливаем is_homepage в False для детальных страниц постов
        }
        return render(request, 'posts/post_detail.html', context)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
            # тут может быть перенаправление или другая логика
    else:
        form = PostForm()  # Создаем пустую форму для GET запроса
    return render(request, 'main/layout.html', {'form': form})


@login_required
@csrf_exempt
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        message = "Unliked"
    else:
        post.likes.add(request.user)
        message = "Liked"
    return JsonResponse({"message": message, "likes_count": post.likes.all().count()})


def liked_posts(request):
    liked_posts = Post.objects.filter(likes=request.user).order_by('-created_at')
    return render(request, 'posts/liked_posts.html', {'posts': liked_posts, 'is_homepage': True})