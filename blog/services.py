from django.db.models import Count
from django.db.models.query import Prefetch, Q
from .models import Post, Comment


""" Бизнес-логика """


def get_post(slug):
    _defer_list = ('author__date_joined', 'author__is_active',
                   'author__is_staff', 'author__is_superuser',
                   'author__password', 'author__username',
                   'author__email', 'author__last_login')
    try:
        return Post.objects.filter(
            slug=slug
            ).select_related(
            'author', 'category'
            ).prefetch_related(
                Prefetch(
                    'comments',
                    Comment.objects.filter(
                        parent__isnull=True
                        ).annotate(likes_count=Count('likes'))
                         .select_related('author')
                         .prefetch_related(
                            Prefetch(
                                'children',
                                Comment.objects.annotate(likes_count=Count('likes'))
                                               .select_related('author').defer(*_defer_list)))
                         .order_by('-date_pub').defer(*_defer_list))
            ).annotate(
            likes_count=Count('likes')
            ).get()
    except Post.DoesNotExist:
        return None


def _get_posts(posts):
    return posts.prefetch_related('tags'
                                  ).select_related(
                                        'category', 'author'
                                  ).order_by(
                                        '-date_pub'
                                  ).defer(
                                            'text', 'is_published', 'author__avatar', 'author__date_joined',
                                            'author__is_active', 'author__is_staff', 'author__is_superuser',
                                            'author__password', 'author__username', 'author__email',
                                            'author__last_login'
                                  ).annotate(comments_count=Count('comments'))


def get_filtered_posts(**filter_kwargs):
    return _get_posts(Post.objects.filter(**filter_kwargs))


def get_searched_posts(search_text):
    return _get_posts(
                      Post.objects.filter(
                                          Q(is_published=True) &
                                          Q(title__icontains=search_text) |
                                          Q(preview_text__icontains=search_text) |
                                          Q(text__icontains=search_text)))


def get_tagged_posts(tag):
    return _get_posts(tag.posts.filter(is_published=True))


def handle_like(liked_object, user_id):
    if liked_object.likes.filter(pk=user_id).exists():
        liked_object.likes.remove(user_id)
    else:
        liked_object.likes.add(user_id)
