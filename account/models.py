from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from friendships.models import FriendList, FriendUtilities
from .utils import get_default_profile_image, get_profile_image_filepath

# Create your models here.


# create a new user
# create a superuser

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username.lower(),
        )

        user.set_password(password)
        user.save(using=self._db)

        FriendList.objects.create(user=user)
        FriendUtilities.objects.create(user=user)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username.lower(),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        


class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    bio = models.TextField(max_length=1000, null=True, blank=True, default="")
    profile_link1_text = models.CharField(max_length=30, null=True, blank=True, default="")
    profile_link1 = models.CharField(max_length=50, null=True, blank=True, default="")
    profile_link2_text = models.CharField(max_length=30, null=True, blank=True, default="")
    profile_link2 = models.CharField(max_length=50, null=True, blank=True, default="")
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True