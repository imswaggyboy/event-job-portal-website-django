import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Post,PostComments
# from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector
from django.urls import reverse_lazy
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .form import CommentPostForm,SearchForm
from django.core.mail import send_mail


# Create your views here.




def post_search(request):
    form = SearchForm()
    query = None
    results =[]

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
            search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(request,
                    'blog/post/search.html',
                    {'form': form,
                    'query': query,
                    'results': results})

# def post_tag_view(request,id):
#     post = Post.published.all()
#     tag  = get_object_or_404(Tag, id=id)
#     posts = post.filter(tags__in=[tag])
#     context = {
#         'posts':posts,
#         'tag':tag
#     }
#     return render(request, 'blog/post/tag_posts.html', context)
    




def like_post(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,id=pk)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)
        return redirect(post.get_absolute_url())
    else:
        messages.error(request,"You need to login first")
        return redirect('login')

def like_comment(request, pk):
    """Handle user likes on comments"""
    if request.user.is_authenticated:
        comment = get_object_or_404(PostComments,
                                id=pk)
        if request.user in comment.comment_likes.all():
            comment.comment_likes.remove(request.user)
        else:
            comment.comment_likes.add(request.user)
        return redirect(comment.post.get_absolute_url())
    else:
        messages.error(request,'Please Login First!')
        return redirect('login')

def post_details(request,year,month,day,slug,pk):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             id = pk,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    if request.method == 'POST':
        if request.user:
            comment = None
            form = CommentPostForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                #assigned the comment to post
                comment.post = post
                comment.name = request.user
                #save the comment
                comment.save()
                return redirect(post.get_absolute_url())
                
    else:
        form = CommentPostForm()
    
    return render(request, 'blog/post/post_detail.html', {'post':post, 'comment_form':form})


# class PostDetailView(DetailView):
#     model = Post


class PostListView(ListView):
    '''
    alternative post view
    '''
    queryset= Post.published.all()
    context_object_name='posts'
    paginate_by =4
    template_name='blog/post/list.html'



# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list,3)
#     page_number = request.GET.get('page',1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request,'blog/post/list.html',{'posts':posts})


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','body','status']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','body','image']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post =self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post =self.get_object()
        if self.request.user==post.author:
            return True
        return False



# def post_share(request, post_id):
#     sent=False
#     post = get_object_or_404(Post,
#                              id=post_id,
#                              status=Post.Status.PUBLISHED)
#     if request.method=='POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd  = form.cleaned_data
#             post_url = request.build_absolute_uri(
#                 post.get_absolute_url()
#             )
#             subject = f"{cd['name']} recommends you to read"\
#             f"{post.title}"

#             sender = f"{cd['email']}"

#             message = f"Read {post.title} at {post_url}\n\n" \
#             f"{cd['name']}\'s comments: {cd['comment']}"

#             # send_mail(subject,message,sender,[cd['to']])
#             send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
#                 #   auth_user=os.environ.get('EMAIL_USER'),
#                 #   auth_password=os.environ.get('EMAIL_PASS'))
#             sent=True
#     else:
#         form = EmailPostForm()
#     return render(request,'blog/post/share.html',{
#         'post':post,
#         'form':form,
#         'sent':sent
#     })