from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=45, help_text="Title of the news post.")
    time = models.DateTimeField(help_text="The time this post was created.")
    text = models.TextField(help_text="Content of the news post, HTML is unescaped.")
    commenting = models.BooleanField(default=True, help_text="Is commenting allowed or not.")
    poster = models.ForeignKey(User, help_text="The user that created the post.")

    def __unicode__(self):
        return self.title


class NewsComment(models.Model):
    news_post = models.ForeignKey(News, help_text="The news post this was posted on.")

    name = models.CharField(max_length=100, blank=True, help_text="The nickname posted under.")

    text = models.TextField(help_text="Content of the comment, HTML is escaped.")

    mail = models.CharField(max_length=200, blank=True, help_text="Email address given by the author.")

    poster = models.ForeignKey(User, null=True, blank=True, help_text="User account that posted this if available.")

    time = models.DateTimeField(help_text="The time this comment was posted.")

    def __unicode__(self):
        return "{:s} ({:s})".format(self.nickname, self.poster)
