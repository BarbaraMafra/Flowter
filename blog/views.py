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
from django.http import JsonResponse

from friendship.exceptions import AlreadyExistsError
from friendship.models import Block, Follow, Friend, FriendshipRequest

# friendship
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block

#from minhas_tags import teste_dahora

def home(request):
    if request.user.is_authenticated():
        lista_amigos = [request.user]
        for usuario in Friend.objects.friends(request.user):
            lista_amigos.append(usuario)
        context = {
            'posts': Post.objects.filter(author__in=lista_amigos).order_by("-date_posted")
        }
        #print(a[0].get_author()) # TESTE MEUaaa
    else: 
        context = {
            'posts':[]
    return render(request, 'blog/home.html', context)

def verifica_seguindo(request, nominho=None):
    # pega todos os colegas
    try:
        friend_list = Friend.objects.friends(request.user)
    except:
        print('failed to get friend list')
    
    seguindo = False
    for i in friend_list:
        if i.get_username() == nominho:
            seguindo = True
    return seguindo

# lista solicitaçõe enviadas
def verifica_request_enviado(request, nominho=None):
    for r in Friend.objects.sent_requests(user=request.user):
        if str(r.to_user) == nominho:
            return True
    return False

# pega o id do request enviado
def get_request_enviado(request, nominho=None):
    for r in Friend.objects.sent_requests(user=request.user):
        if str(r.to_user) == nominho:
            return r
    return False

# lista solicitações de amizade
def verifica_request_recebidos(request, nominho=None):
    for friend_request in Friend.objects.unread_requests(user=request.user):
        if str(friend_request.from_user) == nominho:
            return True
    return False

# pega o id do request recebio
def get_request_recebido(request, nominho=None):
    for r in Friend.objects.unread_requests(user=request.user):
        if str(r.from_user) == nominho:
            return r
    return False

def profile(request, nominho=None):
    a = Friend.objects.unrejected_requests(user=request.user)
    for i in a:
        print(i.from_user_id)
    a = Post.objects.order_by("-date_posted") # todos os posts
    b = [] # onde sera armazenado os posts necessários pra pagina
    c = Profile.objects.all() # todos os perfis

    # pega todos os colegas
    # try:
    #     friend_list = Friend.objects.friends(request.user)
    # except:
    #     print('failed to get friend list')
    
    # seguindo = False
    # for i in friend_list:
    #     if i.get_username() == nominho:
    #         seguindo = True


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
        'posts': b,
        'seguindo': verifica_seguindo(request, nominho),
        'solicitado': verifica_request_enviado(request, nominho),
        'eu_mesmo': request.user.get_username() == nominho
    }
    print(context)
    return render(request, 'blog/profile.html', context)

def search(request):
    nominho = request.GET.get('nominho', '')
    d = {
        'usuarios': []
    } # dicionario que contem informação de todos os perfis achados
    perfis = Profile.objects.all()
    for perfil in perfis:
        if(nominho.lower() in perfil.get_username().lower()):
            usuario = {
                'perfil': perfil,
                'seguindo': verifica_seguindo(request, perfil.get_username()),
                'solicitado': verifica_request_enviado(request, perfil.get_username()),
                'eu_mesmo': request.user.get_username() == perfil.get_username()
            }
            d['usuarios'].append(usuario)
    return render(request, 'blog/search.html', d)
# api do cancel request
def cancel_request(request):
    nominho = request.GET.get('nominho', '')
    id_do_request = get_request_enviado(request, nominho)
    id_do_request.cancel()
# api pra aceitar colega
def accept_request(request):
    nominho = request.GET.get('nominho', '')
    id_do_request = get_request_recebido(request, nominho)
    print(id_do_request)
    print(nominho)
    id_do_request.accept()
# api para recusr amigo
def reject_request(request):
    nominho = request.GET.get('nominho', '')
    id_do_request = get_request_recebido(request, nominho)
    id_do_request.cancel()
# api pra remover amigo
def rm_amigo(request):
    amigo_a_remover = request.GET.get('amigo_a_remover', '')
    perfis = Profile.objects.all()
    a_remover = None

    for perfil in perfis:
        if(amigo_a_remover.lower() in perfil.get_username().lower()):
            a_remover = perfil.user

    Friend.objects.remove_friend(request.user, a_remover)
# api pra add amigo
def add_amigo(request):
    destinatario = request.GET.get('destinatario', '')
    perfis = Profile.objects.all()
    for p in perfis:
        if p.get_username() == destinatario:
            perfil = p
    #print('id do cara:', perfil.user_id)
    #print(request.user.id)
    data = {
        'username': perfil.get_username(),
        'meuzamigo': [],
        'sucesso': False
    }
    try:
        Friend.objects.add_friend(
            request.user,                    # The sender
            perfil.user,                     # The recipient
        )
        data['sucesso'] = True
    except:
        print('failed to add FRIEND cuz yes')
        data['sucesso'] = False
    # try:
    #     friend_request = FriendshipRequest.objects.get(to_user=perfil.user)
    # except:
    #     print('failed to get friend list')
    # try:
    #     friend_request.accept()
    # except:
    #     print('failed to accept request')

    # retorna um jefferson com a lista de amigos
    # e o usuario :thumbsup:
    a = Friend.objects.friends(request.user)
    for i in a:
        data['meuzamigo'].append(i.get_username())
    return JsonResponse(data)

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