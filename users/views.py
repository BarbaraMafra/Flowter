from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from .models import Profile
from django.contrib.auth.models import User

# for use with api
import requests
import json
import os

@login_required
def delaccount(request):
    print('em teoria isso ta deletado')
    u = User.objects.get(username = request.user.get_username())
    u.delete()
    return redirect('blog-home')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sua conta foi criada! Você já pode entrar na sua conta!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Sua conta foi atualizada!')
            
            # send data to api
            # esse [1:] remove o / do /media para que a imagem possa ser encontrada
            files = {'image': open(request.user.profile.image.url[1:], 'rb')}
            response = requests.post('https://api.imgbb.com/1/upload?key=5343cb7d6d9322041daff19a67901f2d', files=files)
            if response.status_code == 200:
                request.user.profile.image_url = response.json()['data']['image']['url']
                request.user.profile.save()
                print(request.user.profile.image_url)
            else:
                print('Tem algo de errado com a api')
                print(response.content)
            
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)