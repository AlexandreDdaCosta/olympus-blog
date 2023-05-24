from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class Graphic(models.Model):
    url_path = models.URLField(max_length=255,
                               null=False)
    name = models.CharField(max_length=255,
                            null=False)
    caption = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['url_path', 'name'],
                                    name='unique_graphic'),
        ]

    def __unicode__(self):
        return '%s/%s' % (self.url_path, self.name)


class Topic(models.Model):
    description = models.CharField(max_length=255)
    graphic = models.ForeignKey(Graphic,
                                on_delete=models.CASCADE)
    name = models.CharField(db_index=True,
                            max_length=30,
                            unique=True,
                            default="/")

    def __unicode__(self):
        return '%s' % (self.name)


class Article(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    body = models.TextField(null=True)
    create_date = models.DateTimeField(_('Created'),
                                       auto_now_add=True)
    featured = models.BooleanField(null=True,
                                   default=False)
    featured_graphic = models.ForeignKey(Graphic,
                                         on_delete=models.CASCADE,
                                         null=True)
    graphics = models.ManyToManyField(Graphic,
                                      related_name='article_graphics')
    published = models.BooleanField(default=False)
    summary = models.TextField(null=True)
    title = models.CharField(db_index=True,
                             max_length=255)
    topic = models.ForeignKey(Topic,
                              on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s' % (self.title)


class Article_Revision(models.Model):
    archive_date = models.DateTimeField(_('Archived'),
                                        auto_now_add=True)
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE)
    body = models.TextField()
    summary = models.TextField(null=True)
    title = models.CharField(db_index=True,
                             max_length=255)
    topic = models.ForeignKey(Topic,
                              on_delete=models.CASCADE,
                              null=True)

    def __unicode__(self):
        return '%s' % (self.title)


class Keyword(models.Model):
    hashtag = models.BooleanField(null=True,
                                  default=False)
    name = models.CharField(db_index=True,
                            max_length=255)

    def __unicode__(self):
        return '%s' % (self.name)


class Keyword_Article(models.Model):
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword,
                                on_delete=models.CASCADE)
    occurrences = models.PositiveIntegerField()

    def __unicode__(self):
        return '%s' % (self.keyword)
