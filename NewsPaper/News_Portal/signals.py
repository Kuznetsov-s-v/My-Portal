import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from .tasks import celery_notify_subscribers


'''
@receiver(m2m_changed, sender=Post.ManyToManyCategory.through)
def notify_subscribers_add_news(sender, instance, **kwargs):
    categories = instance.category.all()
    print('all_categories', categories)

    for category in categories:

        print('category_selected', category)

        subscribers = Subscriber.objects.filter(category=category.id).values('user')
        print(subscribers, 'subscribers')

        for subscriber in subscribers:
            subscriber = subscriber.get('user', None)
            print(subscriber, 'id user / variable subscriber')

            # отправляем письмо

            user_subscriber_username = User.objects.get(pk=subscriber).username
            user_subscriber_email = User.objects.get(pk=subscriber).email
            print(user_subscriber_username, 'user_subscriber_username')
            print(user_subscriber_email, 'user_subscriber_email')

            html_content = render_to_string(
                'letter_to_subscribers_news_created.html',
                {
                    'new_post': instance,
                    'username': user_subscriber_username,
                }
            )
            #'' #'
            msg = EmailMultiAlternatives(
                subject=f'{instance.title} ',
                body=instance.body[:50],
                from_email='qwertyuytrewqwerghbvcds@mail.ru',
                to=[user_subscriber_email]
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем'#'#'
            subject=f'"Здравствуй, {User.username}. Новая статья в твоём любимом разделе(celery)!"'\
                    f'{instance.header_post}',
            from_email='qwertyuytrewqwerghbvcds@mail.ru',
            celery_notify_subscribers.delay(subject, from_email, email, html_content)
'''

@receiver(m2m_changed, sender=Post.ManyToManyCategory.through)
def notify_subscribers(instance, action, *args, **kwargs):
    if action == 'post_add':
        users_emails = [
                user.email
                for category in instance.post_category.all()
                for user in category.subscribers.all()
            ]
        for email in users_emails:
            user = User.objects.get(email=email)
            html_content = render_to_string('mail_created.html', {'post_mail': instance}, )

            subject=f'"Здравствуй, {user.username}. Новая статья в твоём любимом разделе(celery)!"'\
                    f'{instance.header_post}'
            from_email='qwertyuytrewqwerghbvcds@mail.ru',
            celery_notify_subscribers.delay(subject, from_email, email, html_content)

#@receiver(pre_save, sender=Post)
#def check_post_author_by_date(sender, instance, **kwargs):
#    print('check post author')
#    quantity_posts = sender.objects.filter(author=instance.author, date_time_create__date=datetime.datetime.now().date())
#    print('количество статей', len(quantity_posts))
#
#    if len(quantity_posts) < 4:
#        return len(quantity_posts)
#    else:
#        return