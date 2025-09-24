import random
import uuid

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin,send_mail)
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,username,phone_number,password,is_staff,is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('Users must have username')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone_number=phone_number,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        if not extra_fields.get('no password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, phone_number=None,password = None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@',1)[0]
            elif phone_number:
                username =  random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            else:
                raise ValueError('Either username, email or phone_number must be provided')

        while User.objects.filter(username=username).exists():
                username += str(random.randint(10,99))
        return self._create_user(email,username,phone_number,password,False,False, **extra_fields)

    def create_superuser(self, email,username,phone_number,password,**extra_fields):
        return self._create_user(email,username,phone_number,password,True,True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=20, unique=True,
                                help_text=_('Required. 20 characters or fewer. Letters'),
                                validators=[validators.RegexValidator(
                                    r"^[a-zA-z][a-zA-z0-9\-]*$",
                                    _("Enter a valid username."),
                                    "invalid"
                                ),],
                                error_messages={"unique":_( "A user with that username already exists."),},
                                            )
    first_name = models.CharField(_('first name'), max_length=20, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True,null=True,unique=True,
                                    validators=[validators.RegexValidator(
                                        r"^989[01239]\d{8}$",_("Enter a valid phone number."),"invalid"
                                    ),],
                                    error_messages={"unique":_( "A user with that phone number already exists."),},)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'),)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active.'),)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen =models.DateTimeField(_('last seen'), null=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
       full_name = '%s %s' % (self.first_name, self.last_name)
       return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        #sends email to the user
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_logged_in_user(self):
        #returns true if user has actually logged in with valid credentials
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(_('nickname'), max_length=30, blank=True)
    avatar = models.ImageField(_('avatar'),upload_to='avatars/',blank=True,null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    gender = models.BooleanField(_('gender'), help_text=_('femail is false , man is true ,null is unset'),null=True)
    Province = models.ForeignKey(verbose_name=_('province'),to = 'Province', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    @property
    def get_first_name(self):
        return self.user.first_name
    @property
    def get_last_name(self):
        return self.user.last_name
    def get_nickname(self):
        return self.nickname

class Device(models.Model):
        WEB = 1
        IOS = 2
        ANDROID = 3
        DEVICE_TYPES_CHOICES =(
            (WEB , _("WEB")),
            (IOS , _("IOS")),
            (ANDROID , _("ANDROID")),
        )
        user = models.ForeignKey(User,related_name='devices', on_delete=models.CASCADE)
        device_uuid = models.UUIDField(_('device uuid'),null=True)
        last_login = models.DateTimeField(_('last login'),null=True)
        device_type = models.PositiveSmallIntegerField(_('device type'),choices=DEVICE_TYPES_CHOICES,default=ANDROID)
        device_os = models.CharField(_('device OS'),max_length=20 ,blank=True)
        device_model = models.CharField(_('device model'),max_length=50,blank=True)
        app_version = models.CharField(_('app version'),max_length=20,blank=True)
        created_time = models.DateTimeField(_('created time'),auto_now_add=True)

        class Meta:
            db_table = 'device'
            verbose_name = _('device')
            verbose_name_plural = _('devices')

class Province(models.Model):
     name = models.CharField( max_length=50)
     is_valid = models.BooleanField(default=True)
     modified_time = models.DateTimeField( auto_now=True)
     created_time = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.name