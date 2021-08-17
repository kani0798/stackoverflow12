from django.db import models

from account.models import CustomUser


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='problems')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE,
                                related_name='images')

class Reply(models.Model):
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE,
                                related_name='replies')
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='reply_images')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:15] + '...'

    class Meta:
        ordering = ('-created', )


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='comments')
    reply = models.ForeignKey(Reply,
                              on_delete=models.CASCADE,
                              related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created', )

