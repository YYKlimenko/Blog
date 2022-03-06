from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models.query import Prefetch
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from .services import (get_post, get_filtered_posts, get_searched_posts, get_taged_posts, get_category,
                       get_tag, handle_like)


class ShowPost(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_queryset(self):
        return get_post(slug=self.kwargs['post_slug'])

    def get_success_url(self):
        return reverse_lazy('blog:post',
                            kwargs = {'category_slug':self.object.category.slug, 'post_slug':self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.POST.get('like'):
            if request.POST.get('like') == 'post':
                liked_object = self.object
            else:
                Comment.objects.get(pk=request.POST.get('like'))
            handle_like(liked_object, self.request.user.id)
            anchor = request.POST.get('like')

        elif request.POST.get('text'):
            parent_id = request.POST.get('parent')
            anchor = parent_id if parent_id else 'comments'
            Comment.objects.create(text=request.POST.get('text'),
                                   post_id=self.object.pk,
                                   author_id=self.request.user.id,
                                   parent_id=parent_id)

        return HttpResponseRedirect(f'{self.get_success_url()}#{anchor}')


class MainPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 5
    title = 'Главная страница'
    queryset = get_filtered_posts(is_published = True)


    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = self.title
        return context


class PostCatListView(MainPostListView):


    def get_queryset(self):
        self.title = get_category(slug=self.kwargs["category_slug"])
        return get_filtered_posts(is_published = True,
                                  category=self.title)


class PostTagListView(MainPostListView):

    def get_queryset(self):
        self.title = get_tag(slug=self.kwargs['tag_slug'])
        return get_taged_posts(self.title)


class SearchPostListView(MainPostListView):
    title = 'Поиск'

    def get_queryset(self):
        return get_searched_posts(self.search)

    def get(self, request):
        self.search = request.GET.get('text')
        return super().get(self, request)


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')



