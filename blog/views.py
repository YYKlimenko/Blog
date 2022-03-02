from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.db.models.query import Prefetch
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import Post, Tag, Comment
from .forms import AddCommentForm, SearchForm
from .funcs import control_empty
from .services import get_post, get_all_posts, get_searched_posts, get_posts_with_tag

class ShowPost(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    form_class = AddCommentForm

    def get_queryset(self):
        return get_post(slug=self.kwargs['post_slug'])

    def get_success_url(self):
        return reverse_lazy(
                           'blog:post',
                           kwargs = {'category_slug':self.object.category.slug, 'post_slug':self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        like = request.POST.get('like')
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
    paginate_by = 5
    form_class = SearchForm

    def get_success_url(self):
         return reverse_lazy('searcher:find')


class PostListView(PostListData, ListView):


    def get_queryset(self):
        return get_all_posts(is_published = True)


class PostCatListView(PostListData, ListView):

    def get_queryset(self):
        return get_all_posts(is_published = True,
                             category__slug=self.kwargs['category_slug'])


class PostTagListView(PostListView):

    def get_queryset(self):
        return get_posts_with_tag(self.kwargs['tag_slug'])


class SearchPostListView(PostListData, ListView):

    def get_queryset(self):
        return get_searched_posts(self.search)

    def post(self, request):
        self.search = request.POST.get('text')
        return self.get(self, request)


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')



