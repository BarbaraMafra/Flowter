from django import template
from users.models import Profile
from django.contrib.auth.models import User
from friendship.models import Block, Follow, Friend

register = template.Library()

@register.simple_tag
def teste_dahora(user):
    friendship_request = Friend.objects.requests(user)
    perfis = Profile.objects.all()
    d = {
        'solicitacoes': []
    }
    for i in friendship_request:
        username = i.from_user
        for perfil in perfis:
            if perfil.get_username() == str(username):
                url = perfil.image.url
                usuario = {
                    'url': url,
                    'nome': str(username)
                }
                d['solicitacoes'].append(usuario)
    return d
@register.simple_tag
def tem_mais_que_zero(user):
    return len(Friend.objects.requests(user)) > 0
@register.simple_tag
def solicitou_amizade(user, nominho=None):
    for usuario in Friend.objects.requests(user):
        if str(usuario.from_user) == nominho:
            return True
    return False