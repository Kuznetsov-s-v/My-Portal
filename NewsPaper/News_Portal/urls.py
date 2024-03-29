from django.urls import path
# Импортируем созданное нами представление
#from .views import PostList, PostDetail
from .views import PostList, PostDetail, SearchList, PostCreateView, PostUpdateView, PostDeleteView, subscribe, unsubscribe
urlpatterns = [

    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostList.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view() , name='post_detail'),
    path('search', SearchList.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание статьи
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
]