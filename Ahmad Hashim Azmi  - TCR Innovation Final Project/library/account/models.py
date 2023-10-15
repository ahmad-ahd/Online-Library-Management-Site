from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from home.models import Books

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_picture = models.ImageField(default = "images/profile_pictures/default_pfp.png", upload_to = "images/profile_pictures")

    def __str__(self):
        return self.user.username
    
    @receiver(pre_delete, sender = User)
    def delete_user_profile(sender, instance, **kwargs):
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.delete()
        except UserProfile.DoesNotExist:
            pass

    pre_delete.connect(delete_user_profile, sender = User)



class MyBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user.username} - Books: {self.book.title}"