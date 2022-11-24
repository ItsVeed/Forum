# forum/urls.py

from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User routes
    path('user/<str:pk>/', views.RetrieveUser.as_view(), name='user'),

    # Profile routes
    path('profile/<str:pk>/', views.RetrieveProfile.as_view(), name='profile'),

    # Stats routes
    path('stats/', views.RetrieveStats, name='stats'),

    # Section routes
    path('sections/', views.ListSection.as_view(), name='sections'),

    # Category routes
    path('category/<int:pk>/', views.RetrieveCategory, name='category'),

    # Post routes
    path('posts/', views.ListPost.as_view(), name='posts'),
    path('post/<int:pk>/', views.RetrievePost.as_view(), name='post'),
    path('post/create/', views.CreatePost.as_view(), name='post-create'),
    path('post/<int:pk>/like/', views.LikePost, name='post-like'),
    path('post/<int:pk>/delete/', views.DestroyPost.as_view(), name='post-delete'),
    path('post/search/<str:query>/', views.SearchPost, name='post-search'),

    # Comment routes

    path('comment/create/', views.CreateComment.as_view(), name='comment-create'),
    path('comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='comment-delete'),
    path('comment/<int:pk>/like/', views.LikeComment, name='comment-like')
]