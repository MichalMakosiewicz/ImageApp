from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Image(models.Model):
    image = models.ImageField()
    # user = models.ForeignKey(User, on_delete=models.PROTECT)


class UserPlan(models.Model):
    name = models.CharField(max_length=50)
    small_thumbnail_size = models.PositiveIntegerField()
    big_thumbnail_size = models.PositiveIntegerField()
    original_image_link = models.BooleanField()
    is_expiring_link = models.BooleanField()

    def __str__(self):
        return self.name;


class UserProfile(User):
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    plan = models.ForeignKey(UserPlan, on_delete=models.PROTECT)

    def __str__(self):
        return self.username

    @receiver(post_save, sender=User)
    def create_profile_for_user(sender, instance=None, created=False, **kwargs):
        if created:
            UserProfile.objects.get_or_create(user=instance)

    @receiver(pre_delete, sender=User)
    def delete_profile_for_user(sender, instance=None, **kwargs):
        if instance:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.delete()
