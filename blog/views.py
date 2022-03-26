from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Post, Comment, Category, Tag
from . import services


class ShowPost(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self):
        post = services.get_post(self.kwargs['post_slug'])
        if post:
            return post
        else:
            raise Http404

    def get_success_url(self):
        return reverse_lazy('blog:post',
                            kwargs={'category_slug': self.post.category.slug, 'post_slug': self.post.slug})

    def post(self, request, *args, **kwargs):
        self.post = self.get_object()

        if request.POST.get('like'):
            if request.POST.get('like') == 'post':
                liked_object = self.post
            else:
                liked_object = Comment.objects.get(pk=request.POST.get('like'))
            services.handle_like(liked_object, self.request.user.id)
            anchor = request.POST.get('like')

        elif request.POST.get('text'):
            parent_id = request.POST.get('parent')
            anchor = parent_id if parent_id else 'comments'
            Comment.objects.create(text=request.POST.get('text'),
                                   post_id=self.post.pk,
                                   author_id=self.request.user.id,
                                   parent_id=parent_id)
        else:
            raise Http404

        return HttpResponseRedirect(f'{self.get_success_url()}#{anchor}')


class MainPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 5
    title = 'Главная страница'
    queryset = services.get_filtered_posts(is_published=True)

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = self.title
        return context


class PostCatListView(MainPostListView):

    def get_queryset(self):
        self.title = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        return services.get_filtered_posts(is_published=True,
                                           category=self.title)


class PostTagListView(MainPostListView):

    def get_queryset(self):
        self.title = get_object_or_404(Tag, slug=self.kwargs["tag_slug"])
        return services.get_tagged_posts(self.title)


class SearchPostListView(MainPostListView):
    title = 'Поиск'

    def get_queryset(self):
        return services.get_searched_posts(self.search)

    def get(self, request):
        self.search = request.GET.get('text')
        return super().get(self, request)


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')



