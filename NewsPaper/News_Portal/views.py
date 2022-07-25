# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from datetime import datetime
from django.views import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод

from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail, EmailMultiAlternatives


# список новостей
class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'auto_data'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None

        # context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

# отдельная новость
class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user not in Category.subscribers.all():
            context['subscribers'] = True
        else:
            context['subscribers'] = False
        return context

# поиск новости
class SearchList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'auto_data'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 1
    form_class = PostForm

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        # context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['next_sale'] = None

        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

# добавление новости
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('News_Portal.add_Post', )



    def post(self, request, *args, **kwargs):
        post_mail = Post(post_author=request.POST.get('author'),
                         news_post=request.POST.get('ManyToManyCategory'),
                         header_post=request.POST.get('header'),
                         text_post=request.POST.get('text'),
                         post_category=request.POST.get('post_category'))
        post_mail.save()

        # получаем наш html
        html_content = render_to_string(
            'mail_created.html',
            {
                'news_': post_mail,
            }
        )
        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject = f'Здравствуй. {post_mail.post_author} Новая статья в твоём любимом разделе!',
            body = post_mail.text_post[:50] + "...",
            from_email = 'rbt-service@yandex.ru',
            to = ['rbt-service@yandex.ru'],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('news/')
# остановился на том что бы настроить settings!!!!!!!!!!!!!
# дженерик для редактирования объекта
@method_decorator(login_required, name='dispatch')
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    permission_required = ('News_Portal.change_Post', )
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления объекта
@method_decorator(login_required, name='dispatch')
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('News_Portal.delete_Post', )


# функция в которую нужно передавать id статьи и для всех
# категорий этой статьи добавлять пользователя в subscribers
# (пользователя достаем из request.user)
@login_required
def subscribe(request, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    category = post.ManyToManyCategory.all().get(pk=kwargs['pk'])
    user = request.user
    if user not in category.subscribers.all():
        category.subscribers.add(user)
    print(f'{user} подписался {category}')  # для примера вывела на экран пользователя
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unsubscribe(request, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    category = post.ManyToManyCategory.all().get(pk=kwargs['pk'])
    user = request.user
    if user in category.subscribers.all():
        category.subscribers.remove(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))