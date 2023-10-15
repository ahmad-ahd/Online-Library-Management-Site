from django.db import models

class Books(models.Model):
    title = models.CharField(max_length = 255, null = False, blank = False)
    content = models.FileField(default = 'books/Coming_Soon_Page.jpg', upload_to = 'books/')
    summary = models.TextField(max_length = 500)
    author = models.CharField(max_length = 150)
    category = models.ForeignKey('Categories', on_delete = models.SET_NULL, null=True)
    thumbnail = models.ImageField(default = 'images/book_cover_not_available.jpg', upload_to = 'images/')

    def __str__(self):
        return self.title
    

class Categories(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name