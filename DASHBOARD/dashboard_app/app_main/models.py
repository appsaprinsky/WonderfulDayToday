from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

class Profile(models.Model):
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return str(self.user)



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Create your models here.


class ToDo(models.Model):
    STATUS = (
        ('long', 'Long Run ToDo'),
        ('medium', 'Medium Run ToDo'),
        ('short', 'Short Run ToDo'),
        ('other', 'Others ToDo'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    run = models.CharField(max_length=32, choices=STATUS, default='other')
    titel = models.CharField(max_length=150, blank=True)
    importance = models.CharField(max_length=150, blank=True)
    detailed_description = models.TextField()
    completed = models.BooleanField(null=True, blank=True, default=False)
    creation_date = models.DateField(auto_now_add=True)
    deadline_date = models.DateField()
    # marked as done
    # marked as crossed
    # progression

    def __str__(self):
        return str(self.titel)






class Spendings(models.Model):
    STATUS_SPENDINGS = (
        ('rent', 'Rent Spending'),
        ('insurance', 'Insurance Spending'),
        ('tax', 'Tax Spending'),
        ('medical', 'Medical Spending'),
        ('bills', 'Bills Spending'),
        ('internet', 'Internet Spending'),
        ('food', 'Food Spending'),
        ('cloth', 'Cloth Spending'),
        ('wants', 'Wants Spending'),
        ('emergency', 'Emergency Spending'),
        ('others', 'Others Spending'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=STATUS_SPENDINGS, default='others')
    value = models.FloatField(default=0.0)
    titel = models.CharField(max_length=150, blank=True)
    importance = models.CharField(max_length=150, blank=True)
    detailed_description = models.TextField()
    date_of_spending = models.DateField()
    # marked as done
    # marked as crossed


    def __str__(self):
        return str(self.titel)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/uploads/user_{0}/{1}'.format(instance.user.id, filename)

class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)


@receiver(models.signals.post_delete, sender=UploadFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)