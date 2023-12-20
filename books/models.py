from django.db import models
import uuid


class Book(models.Model):
    owl_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=250)
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    pages = models.IntegerField()
    TYPE_CHOICES = (
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('handmade', 'Handmade')
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    releasedAt = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return self.title
