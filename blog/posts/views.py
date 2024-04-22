from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentForm, PostForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    form = PostForm()
    for post in posts:
        post.is_liked = post.is_liked_by_user(request.user)
    return render(request, 'posts/post_list.html', {'posts': posts, 'form': form , 'is_homepage': True})


def post_detail(request, pk):
    try:
        post = Post.objects.prefetch_related('comments').get(pk=pk)
        comments = post.comments.all()
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=pk)
        else:
            form = CommentForm()
        context = {
            'post': post,
            'comments': comments,
            'form': form,
            'is_homepage': False, # Устанавливаем is_homepage в False для детальных страниц постов
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