import datetime
from django.contrib.auth.models import User
from django.db.models import Sum

from django.conf import settings
from django.db import models


# автор
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3
        rate_post_author = self.post_set.all().aggregate(sum_rating=Sum('rate') * 3)['sum_rating']
        # суммарный рейтинг всех комментариев автора;
        rate_comment = self.user.comment_set.all().aggregate(sum_rating=Sum('rate'))['sum_rating']
        # суммарный рейтинг всех комментариев к статьям автора.
        rate_comment_post = Post.objects.filter(author=self).values(
            'id')  # поиск id поста оставленного автором => query_set
        a = 0
        for i in range(
                len(rate_comment_post)):  # проходим по query_set'у циклом вынимая у него id каждого поста оставленного автором
            x = Comment.objects.filter(post_id=rate_comment_post[i]['id']).values(
                'rate')  # делаем запрос на рейтинг всех записей поста id=i => query_set
            for j in range(
                    len(x)):  # проходим по query_set'у суммируя рейтинги пользователей, далее переходим на следующий post
                a = a + x[j][
                    'rate']  # сколько постов оставил автор, столько запросов будет делать цикл. Не лучшее решение, как смог.

        self.rate = rate_post_author + rate_comment + a
        self.save()

    def __str__(self):
        return self.user.username


# категория
class Category(models.Model):
    Category = models.CharField(max_length=64, default="Default value", unique=True)
    subscribers = models.ManyToManyField(User, through='CategoryUser')


#    def __str__(self):
#        return f'{self.category}'
#
#    def get_emails(self):
#        result = set()
#        for user in self.subscribers.all():
#            result.add(user.email)
#        return result

# связывающая таблица для подписок, какой user на какую категорию подписан
class CategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f'{self.category}'


# пост
class Post(models.Model):
    ManyToManyCategory = models.ManyToManyField(Category, through="PostCategory")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    article = 'AR'
    news = 'NE'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    field_choice = models.CharField(max_length=2, choices=POSITIONS, default=news)

    auto_data = models.DateTimeField(max_length=64, default=datetime.datetime.now())

    header = models.CharField(max_length=64, default="Default value")
    text = models.TextField()
    rate = models.FloatField(default=0.0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        return self.text[0:125] + '...'

    def __str__(self):
        return f'{self.auto_data.title()[:10]}: {self.header}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'


# связывающая таблица пост - категория
class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


# комментарии
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.CharField(max_length=1024)
    auto_data = models.CharField(max_length=64, default=datetime.datetime.now())
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
