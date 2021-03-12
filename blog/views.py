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
from users.models import Profile

def home(request):
    context = {
        'posts': Post.objects.order_by("-date_posted")
    }
    #print(a[0].get_author()) # TESTE MEUaaa
    return render(request, 'blog/home.html', context)

def profile(request, nominho=None):
    a = Post.objects.order_by("-date_posted") # todos os posts
    b = [] # onde sera armazenado os posts necessários pra pagina
    c = Profile.objects.all() # todos os perfis

    # pega as info do user pra colocar no profile
    for i in c:
        if str(i.get_username()) == str(nominho):
            autor = i.get_username()
            url_pic = i
            email = i.get_email()
    
    # verifica se é o usuario que foi digitado na url e pega os posts
    for i in a:
        if str(i.get_author()) == str(nominho):
            b.append(i)

    # informações para serem passadas para o template profile.html
    context = {
        'autor': autor,
        'email': email,
        'url_pic': url_pic,
        'posts': b
    }

    return render(request, 'blog/profile.html', context)

def search(request):
    nominho = request.GET.get('nominho', '')

    encontrados = []
    perfis = Profile.objects.all()
    for perfil in perfis:
        if(nominho.lower() in perfil.get_username().lower()):
            print(f'{nominho} is inside {perfil.get_username()}')
            encontrados.append(perfil)
        
    context = {
        'perfis': encontrados
    }
    return render(request, 'blog/search.html', context)

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