from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.order_by("-date_posted")
    }
    #print(a[0].get_author()) # TESTE MEUaaa
    return render(request, 'blog/home.html', context)

def profile(request, nominho=None):
    a = Post.objects.order_by("-date_posted")
    b = []
    for i in a:
        if str(i.get_author()) == str(nominho):
            b.append(i)
    context = {
        'autor': b[0].get_author(),
        'menino': b[0],
        'posts': b
    }
    print(str(a.query))
    return render(request, 'blog/profile.html', context)

#class Profile(ListView):
#    def piquinha(self):
#        print(self.kwargs)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # Ordem de posts (mais atual para o mais antigo)
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})