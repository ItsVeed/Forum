# forum/serializers.py

from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Section, Category, Post, Comment
from authentication.models import Role

User = get_user_model()


# Regular serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'pk')

class EditProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_pic', 'bio')

class ProfileSerializer(serializers.ModelSerializer):
    num_of_posts = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    num_of_comments = serializers.SerializerMethodField()
    roles_serialized = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'bio', 'profile_pic', 'date_joined', 'num_of_posts', 'num_of_comments', 'posts', 'roles_serialized')
    
    def get_num_of_posts(self, obj):
        count = Post.objects.filter(user=obj).count()
        return count
    
    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj)
        serializer = PostMinSerializer(posts, many=True)
        return serializer.data
    
    def get_num_of_comments(self, obj):
        count = Comment.objects.filter(user=obj).count()
        return count
    
    def get_roles_serialized(self, obj):
        role_ids = [role.pk for role in obj.roles.all() ]
        roles = Role.objects.filter(pk__in=role_ids)
        serializer=RoleSerializer(roles, many=True)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    num_of_posts = serializers.SerializerMethodField()
    num_of_comments = serializers.SerializerMethodField()
    roles_serialized = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'roles', 'num_of_posts', 'num_of_comments', 'profile_pic', 'roles_serialized')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password": "Password fields didn't match."})
        
        return attrs
    
    def get_roles_serialized(self, obj):
        role_ids = [role.pk for role in obj.roles.all() ]
        roles = Role.objects.filter(pk__in=role_ids)
        serializer=RoleSerializer(roles, many=True)
        return serializer.data
    
    def get_num_of_comments(self, obj):
        count = Comment.objects.filter(user=obj).count()
        return count
    
    def get_num_of_posts(self, obj):
        count = Post.objects.filter(user=obj).count()
        return count

class CommentSerializer(serializers.ModelSerializer):
    user_serialized = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('pk', 'comment', 'user_serialized', 'users_liked', 'likes', 'datetimeuploaded')
    
    def get_user_serialized(self, obj):
        serializer = UserSerializer(obj.user)
        return serializer.data

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user_serialized = serializers.SerializerMethodField()
    category_serialized = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('pk', 'title', 'post', 'user_serialized', 'category', 'datetimeuploaded', 'likes', 'users_liked', 'comments', 'category_serialized')
    
    def get_comments(self, obj):
        postCommentQuery = Comment.objects.filter(post=obj.id)
        serializer = CommentSerializer(postCommentQuery, many=True)
        return serializer.data

    def get_user_serialized(self, obj):
        serializer = UserSerializer(obj.user)
        return serializer.data
    
    def get_category_serialized(self, obj):
        c = Category.objects.get(pk=obj.category.pk)
        serializer = CategoryMinSerializer(c)
        return serializer.data

class PostMinSerializer(serializers.ModelSerializer):
    user_serialized = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('pk', 'title', 'pinned', 'comment_count', 'user_serialized', 'datetimeuploaded', 'likes')
    
    def get_user_serialized(self, obj):
        serializer = UserSerializer(obj.user)
        return serializer.data
    
    def get_comment_count(self, obj):
        count = Comment.objects.filter(post=obj).count()
        return count


class CategorySerializer(serializers.ModelSerializer):
    section_name = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('pk', 'name', 'section', 'section_name', 'posts')
    
    def get_posts(self, obj):
        categoryPostQuery = Post.objects.filter(category=obj.id)
        serializer = PostMinSerializer(categoryPostQuery, many=True)
        return serializer.data
    
    def get_section_name(self, obj):
        s = Section.objects.get(pk=obj.section.pk)
        
        return s.name

class CategoryMinSerializer(serializers.ModelSerializer):
    latest_post = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('pk', 'name', 'allowed_roles', 'post_count', 'comment_count', 'latest_post')

    
    def get_latest_post(self, obj):
        p = Post.objects.filter(category=obj).order_by('datetimeuploaded').first()
        serializer = PostMinSerializer(p)
        return serializer.data
    
    def get_comment_count(self, obj):
        count = Comment.objects.filter(post__category=obj).count()
        return count
    
    def get_post_count(self, obj):
        count = Post.objects.filter(category=obj).count()
        return count

class SectionSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ('pk', 'name', 'categories')
    
    def get_categories(self, obj):
        c = Category.objects.filter(section=obj.id).order_by("order")
        serializer = CategoryMinSerializer(c, many=True)
        return serializer.data
    

class FullUserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'posts', 'comments')


# Creation serializers

class CreatePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('title', 'post', 'category')

class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment', 'post')