from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class MediaDBOlympus(models.Model):
    description = models.CharField(max_length=255,
                                   null=False)
    url_path = models.URLField(max_length=200,
                               null=False,
                               unique=True)

    def __unicode__(self):
        return u'%s' % (self.url_path)


class TopicDBOlympus(models.Model):
    name = models.CharField(db_index=True,
                            max_length=100,
                            null=False,
                            unique=True)
    description = models.CharField(max_length=255)
    media = models.ForeignKey(MediaDBOlympus,
                              null=True,
                              on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    def __unicode__(self):
        return u'%s' % (self.name)


class TopicKeywordDBOlympus(models.Model):
    topic = models.ForeignKey(TopicDBOlympus,
                              null=False,
                              on_delete=models.CASCADE)
    keyword = models.CharField(db_index=True,
                               max_length=50,
                               null=False,
                               unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['topic', 'keyword'],
                name='dbolympus_constraint_topic_keyword'),
        ]

    def __unicode__(self):
        return u'Topic: %s, Keyword: %s' % (self.topic, self.keyword)


class ArticleDBOlympus(models.Model):
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


class ArticleFeaturedDBOlympus(models.Model):
    article = models.ForeignKey(ArticleDBOlympus,
                                null=False,
                                on_delete=models.CASCADE)
    media = models.ForeignKey(MediaDBOlympus,
                              null=False,
                              on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'media'],
                name='dbolympus_constraint_article_featured'),
        ]

    def __unicode__(self):
        return u'%s' % (self.article)


class ArticleMediaDBOlympus(models.Model):
    article = models.ForeignKey(ArticleDBOlympus,
                                null=False,
                                on_delete=models.CASCADE)
    media = models.ForeignKey(MediaDBOlympus,
                              null=False,
                              on_delete=models.CASCADE)
    bold_caption = models.CharField(max_length=255,
                                    null=True)
    caption = models.TextField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'media'],
                name='dbolympus_constraint_article_media'),
        ]

    def __unicode__(self):
        return u'Article: %s, Media: %s' % (self.article, self.media)


class ArticleKeywordDBOlympus(models.Model):
    article = models.ForeignKey(ArticleDBOlympus,
                                null=False,
                                on_delete=models.CASCADE)
    keyword = models.CharField(db_index=True,
                               max_length=50,
                               null=False,
                               unique=True)
    occurrences = models.PositiveIntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'keyword'],
                name='dbolympus_constraint_article_keyword'),
        ]

    def __unicode__(self):
        return u'Article: %s, Keyword: %s' % (self.article, self.keyword)


class ArticleTopicDBOlympus(models.Model):
    article = models.ForeignKey(ArticleDBOlympus,
                                null=False,
                                on_delete=models.CASCADE)
    topic = models.ForeignKey(TopicDBOlympus,
                              db_index=True,
                              null=False,
                              on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'topic'],
                name='dbolympus_constraint_article_topic'),
        ]

    def __unicode__(self):
        return u'Topic: %s, Article: %s' % (self.topic, self.article)


class ArticleRevisionDBOlympus(models.Model):
    archive_date = models.DateTimeField(_('Archived'),
                                        auto_now_add=True)
    article = models.ForeignKey(ArticleDBOlympus,
                                null=False,
                                on_delete=models.CASCADE)
    body = models.TextField()
    summary = models.TextField(null=True)
    title = models.CharField(db_index=True,
                             max_length=255)

    def __unicode__(self):
        return 'Article: %s, Archive date: %d' % (self.article,
                                                  self.archive_date)


class ThreadDBOlympus(models.Model):
    name = models.CharField(db_index=True,
                            max_length=100,
                            null=False,
                            unique=True)
    description = models.CharField(max_length=255)
    media = models.ForeignKey(MediaDBOlympus,
                              null=True,
                              on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    def __unicode__(self):
        return '%s' % (self.name)


class ThreadArticleDBOlympus(models.Model):
    article = models.ForeignKey(ArticleDBOlympus,
                                null=False,
                                on_delete=models.CASCADE)
    thread = models.ForeignKey(ThreadDBOlympus,
                               null=False,
                               on_delete=models.CASCADE)
    order = models.IntegerField(MinValueValidator(1),
                                null=False,
                                unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'thread'],
                name='dbolympus_constraint_thread_article'),
        ]

    def __unicode__(self):
        return 'Thread: %s, Article: %s' % (self.thread, self.article)


class CommentDBOlympus(models.Model):
    article = models.ForeignKey(ArticleDBOlympus,
                                null=False,
                                on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               null=True,
                               on_delete=models.SET_NULL)
    body = models.TextField(null=False)
    create_date = models.DateTimeField(_('Created'),
                                       auto_now_add=True)
    deleted = models.BooleanField(null=False)
    edit_date = models.DateTimeField(_('Edited'),
                                     auto_now_add=True)


class CommentParentDBOlympus(models.Model):
    comment = models.OneToOneField(CommentDBOlympus,
                                   on_delete=models.CASCADE,
                                   related_name='comment_parent_comment')
    parent = models.ForeignKey(CommentDBOlympus,
                               on_delete=models.CASCADE,
                               related_name='comment_parent_parent')


class CommentLikeDBOlympus(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    comment = models.OneToOneField(CommentDBOlympus,
                                   on_delete=models.CASCADE)
