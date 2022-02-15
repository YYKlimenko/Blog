from django.shortcuts import redirect
from django.http import HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth import logout, login
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.views import  LoginView
from django.db.models import Count
from django.db.models.query import Prefetch
from django.urls import reverse_lazy, reverse
from blog.models import Post, Tag, Comment, User
from blog.forms import AddCommentForm, RegisterUserForm



# Create your views here.

class ShowPost(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    relations = ['author', 'category']

    form_class = AddCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        defer_list = ['author__date_joined', 'author__is_active',
                    'author__is_staff', 'author__is_superuser',
                    'author__password', 'author__username', 'author__email',
                    'author__last_login']
        comments = Comment.objects.filter(parent__isnull = True).\
            filter(post_id = self.object.pk).\
            annotate(likes_count=Count('likes')).\
            select_related('author').\
            prefetch_related(Prefetch('children', Comment.objects.annotate(likes_count=Count('likes')).select_related('author').
                    defer(*defer_list))).\
            order_by('-date_pub').\
            defer(*defer_list)
        context['comments'] = comments
        return context

    # Метод get_object переопределен — в стандартный запрос добавлены select_related модели
    # Требуемые модели прописываются в поле relations
    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug}).select_related(*self.relations)

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


    def get_success_url(self):
        return reverse_lazy('post', kwargs = {'category_slug':self.object.category.slug, 'post_slug':self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        like = request.POST.get('like', None)
        if like:
            if like == 'post':
                if Post.likes.through.objects.filter(user_id=request.user.id):
                    print('Лайк есть!')
                    Post.objects.get(pk=self.object.pk).likes.remove(self.request.user.id)
                else:
                     print('Лайка нет!')
                     Post.objects.get(pk=self.object.pk).likes.add(self.request.user.id)
                return super().form_valid(form)
            else:
                if Comment.likes.through.objects.filter(user_id=request.user.id, comment_id=like):
                    print('Лайк есть!')
                    Comment.objects.get(pk=like).likes.remove(self.request.user.id)
                else:
                     print('Лайка нет!')
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

class PostView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_published = True).\
            annotate(comments_count=Count('comments')).\
            select_related('category', 'author').\
            prefetch_related('tags').\
            order_by('-date_pub').\
            defer('text', 'is_published', 'author__avatar', 'author__date_joined',
                  'author__is_active', 'author__is_staff', 'author__is_superuser',
                  'author__password', 'author__username', 'author__email',
                  'author__last_login', 'image')

class Post_Cat_View(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs['category_slug']
        ).prefetch_related('tags').select_related('category', 'author')

class Post_Tag_View(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return tag.posts.all().prefetch_related('tags').select_related('category')

class RegisterUser(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = 'login'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'
    success_url = 'index'

    def get_success_url(self):
        return reverse_lazy('index')

def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')

def logout_user(request):
    logout(request)
    return redirect('login')
