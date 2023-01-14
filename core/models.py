from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=5000)
    avatar = models.ImageField(upload_to='avatar', default='default_ykicap.jpg', blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)
    username = None
    first_name = None
    last_name = None
    last_login = None
    is_superuser = None
    is_staff = None
    is_active = None
    date_joined = None
    groups = None
    user_permissions = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

class Message(models.Model):
    by = models.IntegerField()
    to = models.IntegerField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    

class GroupMessage(models.Model):
    by = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    roomID = models.IntegerField()
    

class Group(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey('User', on_delete=models.CASCADE, related_name='group_admin')
    members = models.ManyToManyField('User', related_name='group_members')
    messages = models.ManyToManyField('GroupMessage', blank=True, null=True, default=[])
    avatar = models.ImageField(upload_to='avatar', default='group-default_tpy5bz.png', blank=True, null=True)