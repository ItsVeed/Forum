# forum/views.py

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
import forum.serializers as serializers
from .models import Section, Category, Post, Comment
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

# User

class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), username=self.kwargs['pk'])
        return obj

# Profile

class UpdateUser(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(pk=user.pk)
        return queryset

class RetrieveProfile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), username=self.kwargs['pk'])
        return obj


# Stats

@api_view(['GET'])
@permission_classes([AllowAny])
def RetrieveStats(request):
    post_count = Post.objects.all().count()
    comment_count = Comment.objects.all().count()
    user_count = User.objects.all().count()
    latest_user = serializers.UserSerializer(User.objects.order_by('-date_joined').first()).data

    response = {
        'post_count': post_count,
        'comment_count': comment_count,
        'user_count': user_count,
        'latest_user': latest_user
    }

    
    return Response(response, status=status.HTTP_200_OK)

# Section views

class ListSection(generics.ListAPIView):
    queryset = Section.objects.all().order_by("order")
    serializer_class = serializers.SectionSerializer
    permission_classes = [AllowAny]


# Category views

def checkRole(user, category_id):
    category = Category.objects.get(pk=category_id)
    category_roles = category.allowed_roles.all()
    if len(category_roles) == 0:
        return True
    if user.is_anonymous:
        return False
    user_roles = user.roles.all()
    for role in user_roles:
        return True
        if category.allowed_roles.filter(pk=role.pk).exists():
            return True
    return False

@api_view(['GET'])
@permission_classes([AllowAny])
def RetrieveCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = serializers.CategorySerializer(category)

    if checkRole(request.user, category.pk):
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# Post views

@api_view(['GET'])
@permission_classes([AllowAny])
def SearchPost(request, query):
    try:
        posts = Post.objects.filter(
            Q(user__username__icontains=query) |
            Q(title__icontains=query) |
            Q(post__icontains=query)
        )

        for post in posts:
            if not checkRole(request.user, post.category.pk):
                posts.remove(post)
        
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = serializers.PostSerializer(posts, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

class ListPost(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        allowed_post_ids = [post.pk for post in Post.objects.all() if checkRole(self.request.user, post.category.pk)]
        query = Post.objects.filter(pk__in=allowed_post_ids).order_by('-datetimeuploaded')
        return query


class RetrievePost(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if not checkRole(self.request.user, obj.category.pk):
            raise PermissionDenied
        return obj

class CreatePost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.CreatePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class DestroyPost(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)
        return queryset

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def LikePost(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if post.users_liked.filter(username=request.user.username).exists():
        post.users_liked.remove(request.user)
        post.save()
        return Response(status=status.HTTP_200_OK)
    else:
        post.users_liked.add(request.user)
        post.save()
        return Response(status=status.HTTP_200_OK)


# Comment views

class CreateComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class DeleteComment(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(user=self.request.user)
        return queryset

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def LikeComment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if comment.users_liked.filter(username=request.user.username).exists():
        comment.users_liked.remove(request.user)
        comment.save()
        return Response(status=status.HTTP_200_OK)
    else:
        comment.users_liked.add(request.user)
        comment.save()
        return Response(status=status.HTTP_200_OK)