from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class Media(models.Model):
    description = models.CharField(max_length=255,
                                   null=False)
    url_path = models.URLField(max_length=200,
                               null=False,
                               unique=True)

    def __unicode__(self):
        return u'%s' % (self.url_path)


class Topic(models.Model):
    name = models.CharField(db_index=True,
                            max_length=100,
                            null=False,
                            unique=True)
    description = models.CharField(max_length=255)
    media = models.ForeignKey(Media,
                              null=True,
                              on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    def __unicode__(self):
        return u'%s' % (self.name)


class TopicKeyword(models.Model):
    topic = models.ForeignKey(Topic,
                              null=False,
                              on_delete=models.CASCADE)
    keyword = models.CharField(db_index=True,
                               max_length=50,
                               null=False,
                               unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['topic', 'keyword'],
                                    name='article_keyword'),
        ]

    def __unicode__(self):
        return u'Topic: %s, Keyword: %s' % (self.topic, self.keyword)


class Article(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    body = models.TextField(null=False)
    create_date = models.DateTimeField(_('Created'),
                                       auto_now_add=True)
    edit_date = models.DateTimeField(_('Edited'),
                                     auto_now_add=True)
    published = models.BooleanField(null=False)
    summary = models.TextField(null=True)
    title = models.CharField(db_index=True,
                             max_length=255)

    def __unicode__(self):
        return u'%s' % (self.title)


class ArticleFeatured(models.Model):
    article = models.ForeignKey(Article,
                                null=False,
                                on_delete=models.CASCADE)
    media = models.ForeignKey(Media,
                              null=False,
                              on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'media'],
                                    name='article_media'),
        ]

    def __unicode__(self):
        return u'%s' % (self.article)


class ArticleMedia(models.Model):
    article = models.ForeignKey(Article,
                                null=False,
                                on_delete=models.CASCADE)
    media = models.ForeignKey(Media,
                              null=False,
                              on_delete=models.CASCADE)
    bold_caption = models.CharField(max_length=255,
                                    null=True)
    caption = models.TextField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'media'],
                                    name='article_media'),
        ]

    def __unicode__(self):
        return u'Article: %s, Media: %s' % (self.article, self.media)


class ArticleKeyword(models.Model):
    article = models.ForeignKey(Article,
                                null=False,
                                on_delete=models.CASCADE)
    keyword = models.CharField(db_index=True,
                               max_length=50,
                               null=False,
                               unique=True)
    occurrences = models.PositiveIntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'keyword'],
                                    name='article_keyword'),
        ]

    def __unicode__(self):
        return u'Article: %s, Keyword: %s' % (self.article, self.keyword)


class ArticleTopic(models.Model):
    article = models.ForeignKey(Article,
                                null=False,
                                on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,
                              db_index=True,
                              null=False,
                              on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'topic'],
                                    name='article_topic'),
        ]

    def __unicode__(self):
        return u'Topic: %s, Article: %s' % (self.topic, self.article)


class ArticleRevision(models.Model):
    archive_date = models.DateTimeField(_('Archived'),
                                        auto_now_add=True)
    article = models.ForeignKey(Article,
                                null=False,
                                on_delete=models.CASCADE)
    body = models.TextField()
    summary = models.TextField(null=True)
    title = models.CharField(db_index=True,
                             max_length=255)

    def __unicode__(self):
        return 'Article: %s, Archive date: %d' % (self.article,
                                                  self.archive_date)


class Thread(models.Model):
    name = models.CharField(db_index=True,
                            max_length=100,
                            null=False,
                            unique=True)
    description = models.CharField(max_length=255)
    media = models.ForeignKey(Media,
                              null=True,
                              on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    def __unicode__(self):
        return '%s' % (self.name)


class ThreadArticle(models.Model):
    article = models.ForeignKey(Article,
                                null=False,
                                on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread,
                               null=False,
                               on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'thread'],
                                    name='article_thread'),
        ]

    def __unicode__(self):
        return 'Thread: %s, Article: %s' % (self.thread, self.article)


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL)
    body = models.TextField(null=False)
    create_date = models.DateTimeField(_('Created'),
                                       auto_now_add=True)
    deleted = models.BooleanField(null=False)
    edit_date = models.DateTimeField(_('Edited'),
                                     auto_now_add=True)


class CommentParent(models.Model):
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                unique=True)
    parent = models.ForeignKey(Comment,
                               on_delete=models.CASCADE)


class CommentLike(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                unique=True)
