from django.http import Http404
from django.db.models import Count
from django.db.models.query import Prefetch, Q
from .models import Post, Comment, Tag


""" Бизнес-логика """

def _list_valid(get_queryset):
        def wrapper(*args, **kwargs):
            posts_list = get_queryset(*args, **kwargs)
            if len(posts_list) == 0:
                raise Http404
            return posts_list
        return wrapper


def get_post(**filter_kwargs):
    defer_list = ('author__date_joined', 'author__is_active',
                      'author__is_staff', 'author__is_superuser',
                      'author__password', 'author__username',
                      'author__email','author__last_login')
    return Post.objects.filter(
                                **filter_kwargs
                                ).select_related('author', 'category'
                                ).prefetch_related(
                                                   Prefetch(
                                                            'comments',
                                                             Comment.objects.filter(
                                                             parent__isnull = True
                                                             ).annotate(likes_count=Count('likes')
                                                             ).select_related('author'
                                                             ).prefetch_related(
                                                             Prefetch(
                                                             'children',
                                                             Comment.objects.annotate(likes_count=Count('likes')
                                                             ).select_related('author'
                                                             ).defer(*defer_list))
                                ).order_by('-date_pub'
                            ).defer(*defer_list)))


@_list_valid
def _get_posts_list(post_list):
    return post_list.prefetch_related('tags'
                                      ).select_related('category', 'author'
                                      ).order_by('-date_pub'
                                      ).defer('text', 'is_published', 'author__avatar', 'author__date_joined',
                                              'author__is_active', 'author__is_staff', 'author__is_superuser',
                                              'author__password', 'author__username', 'author__email',
                                              'author__last_login'
                                      ).annotate(comments_count=Count('comments'))


def get_all_posts(**filter_kwargs):
    return _get_posts_list(Post.objects.filter(**filter_kwargs))


def get_searched_posts(search_text):
    return _get_posts_list(Post.objects.filter(
                                               Q(is_published = True
                                               )&Q(title__icontains=search_text)|
                                               Q(preview_text__icontains=search_text)|
                                               Q(text__icontains=search_text)))


def get_posts_with_tag(tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    return _get_posts_list(tag.posts.filter(is_published = True))

