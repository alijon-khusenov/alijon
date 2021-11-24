from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField('Заголовок',max_length=255)
    text = models.TextField('Содержимое')
    slug = models.SlugField('Ссылка')
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField('Картинка', default='default.jpg', blank=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='article_likes')
    dislikes = models.ManyToManyField(User, related_name='article_dislikes')

    def __str__(self):
        return self.title

    def snippet(self):
        return self.text[:20] + '... read more'

    def shorten(self):
        return self.title[:10] + '...'

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.article, self.body[:5])