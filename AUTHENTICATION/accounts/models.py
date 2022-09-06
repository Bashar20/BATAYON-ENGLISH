from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext as _
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this








class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
    
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    mobile = models.PositiveIntegerField(default=0,unique=True) 
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username","mobile"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    


class Profile(models.Model):   
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
	profile_pic = models.ImageField(default='default.webp',upload_to="PROFILE")

	@receiver(post_save, sender=CustomUser) #add this
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=CustomUser) #add this
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
