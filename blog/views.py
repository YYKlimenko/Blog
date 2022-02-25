from django.http import HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.db.models.query import Prefetch
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from blog.models import Post, Tag, Comment
from blog.forms import AddCommentForm, SearchForm


def control_empty(get_queryset):
        def wrapper(self):
            obj = get_queryset(self)
            if len(obj) == 0:
                raise Http404
            return obj
        return wrapper


class ShowPost(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    form_class = AddCommentForm

    def get_queryset(self):
        return Post.objects.filter(
                                   slug=self.kwargs['post_slug']
                                   ).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        defer_list = ['author__date_joined', 'author__is_active',
                      'author__is_staff', 'author__is_superuser',
                      'author__password', 'author__username',
                      'author__email','author__last_login']

        comments = Comment.objects.filter(
                                          parent__isnull = True
                                          ).filter(post_id = self.object.pk
                                          ).annotate(likes_count=Count('likes')
                                          ).select_related('author'
                                          ).prefetch_related(
                                                             Prefetch(
                                                             'children',
                                                             Comment.objects.annotate(likes_count=Count('likes')
                                                             ).select_related('author'
                                                             ).defer(*defer_list))
                                          ).order_by('-date_pub'
                                          ).defer(*defer_list)
        context['comments'] = comments
        return context

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs = {'category_slug':self.object.category.slug, 'post_slug':self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        like = request.POST.get('like', None)
        if like:
            if like == 'post':
                if Post.likes.through.objects.filter(user_id=request.user.id, post_id=self.object.pk):
                    Post.objects.get(pk=self.object.pk).likes.remove(self.request.user.id)
                else:
                     Post.objects.get(pk=self.object.pk).likes.add(self.request.user.id)
                return super().form_valid(form)
            else:
                if Comment.likes.through.objects.filter(user_id=request.user.id, comment_id=like):
                    Comment.objects.get(pk=like).likes.remove(self.request.user.id)
                else:
                     Comment.objects.get(pk=like).likes.add(self.request.user.id)
                return super().form_valid(form)
        else:
            if form.is_valid():
                form = form.save(commit = False)
                if request.user.is_authenticated:
                    form.author_id = self.request.user.id
                form.post_id = self.object.pk
                if request.POST['parent'] != 'None':
                    form.parent_id = request.POST['parent']
                form.save()
                return super().form_valid(form)


class PostListData(FormMixin):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 2
    form_class = SearchForm

    def get_success_url(self):
         return reverse_lazy('searcher:find')


class PostListView(PostListData, ListView):

    @control_empty
    def get_queryset(self):
        return Post.objects.filter(
                                   is_published = True
                                   ).prefetch_related('tags'
                                   ).select_related('category', 'author'
                                   ).order_by('-date_pub'
                                   ).defer('text', 'is_published', 'author__avatar', 'author__date_joined',
                                           'author__is_active', 'author__is_staff', 'author__is_superuser',
                                           'author__password', 'author__username', 'author__email',
                                           'author__last_login'
                                    ).annotate(comments_count=Count('comments'))


class PostCatListView(PostListData, ListView):
    @control_empty
    def get_queryset(self):
        return Post.objects.filter(
                                   is_published = True,
                                   category__slug=self.kwargs['category_slug']
                                   ).annotate(comments_count=Count('comments')
                                   ).prefetch_related('tags'
                                   ).select_related('category', 'author'
                                   ).order_by('-date_pub'
                                   ).defer('text', 'is_published', 'author__avatar', 'author__date_joined',
                                           'author__is_active', 'author__is_staff', 'author__is_superuser',
                                           'author__password', 'author__username', 'author__email',
                                           'author__last_login', 'image')


class PostTagListView(PostListView):

    @control_empty
    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return tag.posts.filter(
                                is_published = True,
                                ).prefetch_related('tags'
                                ).select_related('category'
                                ).annotate(comments_count=Count('comments')
                                ).prefetch_related('tags'
                                ).select_related('category', 'author'
                                ).order_by('-date_pub'
                                ).defer('text', 'is_published', 'author__avatar', 'author__date_joined',
                                        'author__is_active', 'author__is_staff', 'author__is_superuser',
                                        'author__password', 'author__username', 'author__email',
                                        'author__last_login', 'image')


class SearchPostListView(PostListData, ListView):

    def get_queryset(self):
        return Post.objects.filter(
                                   Q(is_published = True
                                   )&Q(title__icontains=self.search)|
                                   Q(preview_text__icontains=self.search)|
                                   Q(text__icontains=self.search)
                                   ).prefetch_related('tags'
                                   ).select_related('category', 'author'
                                   ).order_by('-date_pub'
                                   ).defer('text', 'is_published', 'author__avatar', 'author__date_joined',
                                           'author__is_active', 'author__is_staff', 'author__is_superuser',
                                           'author__password', 'author__username', 'author__email',
                                           'author__last_login', 'image'
                                   ).annotate(comments_count=Count('comments'))
    def post(self, request):
        self.search = request.POST.get('text', None)
        return self.get(self, request)


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')



