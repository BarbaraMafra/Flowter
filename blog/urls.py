from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('profile/<nominho>/', views.profile, kwargs=None, name='blog-profile'),
    path('search', views.search, kwargs=None, name='blog-search'),
    path('search/', views.search, kwargs=None, name='blog-search'),
    path('friendship/', include('friendship.urls')),
    path('addamigo/', views.add_amigo, kwargs=None, name='addamigo'),
    path('rmamigo/', views.rm_amigo, kwargs=None, name='rmamigo'),
    path('cancelrequest/', views.cancel_request, kwargs=None, name='cancelrequest'),
    path('acceptrequest/', views.accept_request, kwargs=None, name='acceptrequest'),
    path('rejectrequest/', views.reject_request, kwargs=None, name='rejectrequest'),
]
