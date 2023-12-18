from django.db import models


class Lending(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    borrowedAt = models.DateTimeField()
    returnedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} has borrowed {self.book.title}"
