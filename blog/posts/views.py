from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm, PostForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    print(posts)  # Выводит объекты постов в консоль
    return render(request, 'posts/post_list.html', {'posts': posts})


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
        return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
#
#
# @transaction.atomic
# @login_required
# def post_create(request):
#     try:
#         if request.method == 'POST':
#             form = PostForm(request.POST, request.FILES)
#             if form.is_valid():
#                 post = form.save(commit=False)
#                 post.author = request.user
#                 post.save()
#                 # После успешного создания поста перенаправляем на страницу с деталями этого поста
#                 return redirect('post_detail', pk=post.pk)
#         else:
#             form = PostForm()
#         return render(request, 'blog/post_form.html', {'form': form})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
#
#
# @transaction.atomic
# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if post.author != request.user:
#         return JsonResponse({'error': 'You are not authorized to edit this post.'}, status=403)
#
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})
#
#
# @transaction.atomic
# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if post.author != request.user:
#         return JsonResponse({'error': 'You are not authorized to delete this post.'}, status=403)
#
#     if request.method == 'POST':
#         post.delete()
#         return redirect('post_list')
#     return render(request, 'blog/post_delete.html', {'post': post})
#
#
# @transaction.atomic
# @login_required  # Добавляем декоратор, чтобы убедиться, что пользователь аутентифицирован
# def add_comment_to_post(request, pk):
#     try:
#         post = get_object_or_404(Post, pk=pk)
#         if request.method == 'POST':
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.post = post
#                 comment.save()
#                 return redirect('post_detail', pk=post.pk)
#         else:
#             form = CommentForm()
#         return render(request, 'blog/add_comment_to_post.html', {'form': form})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
