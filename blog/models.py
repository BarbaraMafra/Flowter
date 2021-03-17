from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_author(self):
        return self.author


#class Followers(models.Model):
#    seguidor = models.ForeignKey(User, on_delete=models.CASCADE)
#    seguido = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)
#    data_solicitacao = models.DateTimeField(default=timezone.now)
#    ativo = models.BooleanField (blank=True, null=False, default=True)
#
#    def __str__(self):
#        pass