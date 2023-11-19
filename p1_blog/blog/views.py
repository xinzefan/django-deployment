from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404 , redirect
from django.views.generic import (TemplateView, ListView, DetailView,CreateView, UpdateView,DeleteView)
from blog.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from django.utils import timezone
from django.urls import reverse_lazy
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-published_date')

class PostDetaiView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = "/login/"
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url = "/login/"
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = "post_list.html"
    model = Post
    

#########
@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST" : 
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/comment_form.html',{'form':form})
    

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish
    return redirect('blog:post_detail',pk=pk)

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)
 