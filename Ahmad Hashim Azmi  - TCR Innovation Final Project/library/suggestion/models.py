from django.db import models

class Suggestions(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 150)
    year_released = models.PositiveIntegerField(blank = True, null = True)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.title