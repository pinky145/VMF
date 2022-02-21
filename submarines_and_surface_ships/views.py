from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from .models import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin


class RusshipHome(DataMixin, ListView):
    model = Rusship
    template_name = 'submarines_and_surface_ships/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        # context['menu'] = menu
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0
        # context['cats'] = Category.objects.all()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Rusship.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Rusship.objects.all()
#     cats = Category.objects.all()
#
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'submarines_and_surface_ships/index.html', context=context)
#


def about(request):
    contact_list = Rusship.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'submarines_and_surface_ships/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'submarines_and_surface_ships/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'submarines_and_surface_ships/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        # context['cats'] = Category.objects.all()
        return dict(list(context.items()) + list(c_def.items()))


# def contact(request):
#     return HttpResponse("Обратная связь")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'submarines_and_surface_ships/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

#
# def login(request):
#     return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_post(request, post_slug):
#    post = get_object_or_404(Rusship, slug=post_slug)
#
#    context = {
#        'post': post,
#        'menu': menu,
#        'title': post.title,
#        'cat_selected': post.cat_id,
#    }
#
#    return render(request, 'submarines_and_surface_ships/post.html', context=context)


class ShowPost(DataMixin, DetailView):
    model = Rusship
    template_name = 'submarines_and_surface_ships/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        # context['title'] = context['post']
        # context['menu'] = menu
        # context['cats'] = Category.objects.all()
        return dict(list(context.items()) + list(c_def.items()))


class RusshipCategory(DataMixin, ListView):
    model = Rusship
    template_name = 'submarines_and_surface_ships/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Rusship.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # context['cat_selected'] = context['posts'][0].cat_id
        # context['cats'] = Category.objects.all()
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     cats = Category.objects.all()
#     cat = get_object_or_404(Category, slug=cat_slug)
#     posts = Rusship.objects.filter(cat_id=cat.id)
#
#     if len(posts) == 0:
#         raise Http404
#
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': cat.name,
#         'cat_selected': cat.id,
#     }
#
#     return render(request, 'submarines_and_surface_ships/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'submarines_and_surface_ships/register.html'
    # перенаправление на login после успешной регистрации
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'submarines_and_surface_ships/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')