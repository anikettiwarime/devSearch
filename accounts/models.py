import uuid
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from decouple import config

# Create your models here.


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    created = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    def default_profile_image_url():
        cloud_name = config('CLOUDINARY_CLOUD_NAME')
        return f'https://res.cloudinary.com/{cloud_name}/image/upload/v1705074418/phmwod4bzud9j12j8dc0.png'

    profile_image = CloudinaryField('image', default=default_profile_image_url)

    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user.username)

    @property
    def image_url(self):
        return (
            f"https://res.cloudinary.com/{config('CLOUDINARY_CLOUD_NAME')}/{self.profile_image}"
        )


class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(
        max_length=200, null=True, blank=True, default="")

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name="messages")
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.sender.name) + ": " + str(self.subject)

    class Meta:
        ordering = ['is_read', '-created']
