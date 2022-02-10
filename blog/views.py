from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.views import  LoginView
from django.urls import reverse_lazy
from blog.models import Post, Tag
from blog.forms import AddCommentForm


# Create your views here.


class ShowPost(FormMixin, DetailView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    form_class = AddCommentForm

    def get_success_url(self):
        return reverse_lazy('post', kwargs = {'category_slug':self.object.category.slug, 'post_slug':self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
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
        return Post.objects.all().prefetch_related('tags').select_related('category')


class Post_Cat_View(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['category_slug']).prefetch_related('tags').select_related('category')


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
    form_class = UserCreationForm
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
