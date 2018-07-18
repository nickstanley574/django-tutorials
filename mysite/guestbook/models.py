from django.db import models
from django.utils import timezone

#  attributes of the class represent the columns in the datebase
class Comment(models.Model):     
    name = models.CharField(max_length=20)
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__ (self):
        return '<Name: {}, ID: {}>'.format(self.name, self.pk)
