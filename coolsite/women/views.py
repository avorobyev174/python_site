from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from .models import *
from .utils import DataMixin, menu


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    # extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items())) # формирование общего контекста
        # context['menu'] = menu
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Women.objects.all()
#     cats = Category.objects.all()
#
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0
#     }
#     return render(request, 'women/index.html', context=context)


# def show_category(request, cat_id):
#     # return HttpResponse(f"Отображение категории с id = {cat_id}")
#     posts = Women.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id
#     }
#     return render(request, 'women/index.html', context=context)
class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    # extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        # c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
        #                               cat_selected=context['posts'][0].cat_id)
        # context['menu'] = menu
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id
        context = dict(list(context.items()) + list(c_def.items()))  # формирование общего контекста
        return context

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


# @login_required
def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте', 'page_obj': page_obj})


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id
#     }
#
#     return render(request, 'women/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))  # формирование общего контекста
        # context['menu'] = menu
        # context['title'] = context['post']
        return context


# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             # Women.objects.create(**form.cleaned_data)
#             form.save()
#             return redirect('home')
#         # except:
#         #     form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/add_page.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')  # маршрут перенаправления
    # login_url = '/admin/'
    login_url = reverse_lazy('home')  # маршрут перенаправления
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context = dict(list(context.items()) + list(c_def.items()))  # формирование общего контекста
        # context['menu'] = menu
        # context['title'] = 'Добавление статьи'
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')  # маршрут перенаправления

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context = dict(list(context.items()) + list(c_def.items()))  # формирование общего контекста

        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'
    # success_url = reverse_lazy('login')  # маршрут перенаправления

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        context = dict(list(context.items()) + list(c_def.items()))  # формирование общего контекста

        return context

    # def get_success_url(self):
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class Contact(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context = dict(list(context.items()) + list(c_def.items()))  # формирование общего контекста

        return context

    def form_valid(self, form):
        # user = form.save()
        # login(self.request, user)
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизация")


# def categories(request, catid):
#     print(request.GET)
#     return HttpResponse(f"<h1>Статьи</h1><p>{catid}</p>")
#
#
# def archive(request, year):
#     if int(year) > 2020:
#         return redirect('home', permanent=True)
#     return HttpResponse(f"<h1>Архив</h1><p>{year}</p>")
#

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
