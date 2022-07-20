# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from datetime import datetime
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод

from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

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


# отрправляем письмо
#class send_mail(View):
#    def sendMail(self, request, *args, **kwargs):
#        send_mail(
#            author_and_rate=f'{Author.user} {Author.rate}',
#            # имя автора и рейтинг будут в теме для удобства
#            message=appointment.message,  # сообщение с кратким описанием проблемы
#            from_email='peterbadson@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
#            recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
#        )
#
#        return redirect('appointments:make_appointment')