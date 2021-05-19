from django.db import models
from .enums import *


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')

    class Meta:
        abstract = True


class Post(TimestampMixin):
    post_type = models.IntegerField(choices=PostType.choices(), null=False, default=PostType.NEWS.value)
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to='post_images', null=False)

    def __str__(self):
        return '{}: author {}, poster {}, title {}, text {}'.format(self.id, self.author, self.poster, self.title,
                                                                    self.text)


class PostSubscription(TimestampMixin):
    email = models.CharField(max_length=255, null=False)
    subscribe = models.BooleanField(default=True, null=False)
    token = models.CharField(max_length=255, null=False)

    def __str__(self):
        return '{}: email {}'.format(self.id, self.email)


class Slide(TimestampMixin):
    title = models.CharField(max_length=255, null=False)
    subtitle = models.CharField(max_length=255, default=None)
    text = models.CharField(max_length=255, default='', null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to='slides', null=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return '{}: author {}, poster {}, title {}, subtitle {}'.format(self.id, self.author, self.poster,
                                                                        self.title, self.subtitle)


class Video(TimestampMixin):
    title = models.CharField(max_length=255, null=False)
    text = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    poster = models.FileField(upload_to='videos', null=False)
    link = models.CharField(max_length=3000, null=False)

    def __str__(self):
        return '{}: title {}, text {}, author {}, poster {}'.format(self.id, self.title, self.text, self.author,
                                                                    self.poster)


class City(TimestampMixin):
    donation_state = models.BooleanField(null=False, default = True)
    state = models.CharField(max_length=255, null=False)
    title = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return '{}: donation state {}, state {}, title {}'.format(self.id, self.donation_state, self.state, self.title)


class GoldPrice(TimestampMixin):

    gram_in_kzt = models.DecimalField(null=False, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'Gold price'
        verbose_name_plural = 'Gold prices'

    def __str__(self):
        return '{}: price for 1 gram {} tg'.format(self.id, self.gram_in_kzt)


class Principle(TimestampMixin):
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(null=False)
    number = models.IntegerField(null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to='principle_images', null=False)

    class Meta:
        verbose_name = 'Principle'
        verbose_name_plural = 'Principles'

    def __str__(self):
        return '{}: title {}, text {}, author {}, poster {}, number {}'.format(self.id, self.title, self.text,
                                                                               self.author, self.poster, self.number)


class Question(TimestampMixin):
    question_status = models.IntegerField(choices=QuestionStatus.choices(), null=False,
                                          default=QuestionStatus.NEW.value)
    email = models.CharField(max_length=255, null=False)
    message = models.TextField(null=False)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return '{}: question status {}, email {}, message {}'.format(self.id, self.question_status, self.email,
                                                                     self.message)


class Store(TimestampMixin):
    title = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return '{}: title'.format(self.id, self.title)


class Widgets(TimestampMixin):
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to='widget_images', null=False)

    class Meta:
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'

    def __str__(self):
        return '{}: title {}, text {}, author {}, poster {}'.format(self.id, self.title, self.text, self.author,
                                                                    self.poster)


class Volunteers(TimestampMixin):
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to='volunteer_images', null=False)

    class Meta:
        verbose_name = 'Volunteers'
        verbose_name_plural = 'Volunteer'

    def __str__(self):
        return '{}: title {}, text {}, author {}, poster {}'.format(self.id, self.title, self.text, self.author,
                                                                    self.poster)


class Statistics(TimestampMixin):
    title = models.CharField(max_length=255, null=False)
    file = models.FileField(upload_to='statistics', null=True)
    author = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Statistics Item'
        verbose_name_plural = 'Statistics'


class VolunteerRequests(TimestampMixin):
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = 'Volunteer request'
        verbose_name_plural = 'Volunteers requests'

