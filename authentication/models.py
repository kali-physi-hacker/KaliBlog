from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ 


class UserManager(BaseUserManager):
    """Object Manager for the Custom User Model
    """

    def create_user(self, email, first_name, last_name, password=None, commit=True):
        """Creates, saves and returns a user with normal privileges
        :param email:
        :param first_name:
        :param last_name:
        :param password:
        :param commit:
        """

        if not email:
            raise ValueError("User must provide email")

        if not first_name:
            raise ValueError("User must provide first_name")

        if not last_name:
            raise ValueError("User must provide last_name")

        if not password:
            raise ValueError("User must provide password")


        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            #password=password
        )

        user.set_password(password)

        if commit:
            user.save(using=self._db)
        
        return user 

    def create_superuser(self, email, first_name, last_name, password):
        """Creates, saves and returns a user with administrator privileges
        
        :param email:
        :param first_name:
        :param last_name:
        :param password:
        """

        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            commit=False
        )

        user.is_staff = True 
        user.is_superuser = True
        user.save(using=self._db)

        return user 



class User(AbstractBaseUser, PermissionsMixin):
    """The Custom User Model
    """

    email = models.EmailField(
        verbose_name=_("email_address"),
        max_length=255,
        unique=True,
    )

    # password field is provided by the AbstractBaseUser model

    first_name = models.CharField(
        verbose_name=_("first_name"),
        max_length=100,
        blank=True
    )

    last_name = models.CharField(
        verbose_name=_("last_name"),
        max_length=100,
        blank=True
    )

    # is_superuser, groups and permissions are provided by the PermissionsMixin model

    is_active = models.BooleanField(
        _("active status"),
        default=True,
        help_text=_(
            "Designates whether a user is active or not"
            "This is unselected in the case of a delete"    
        )
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether a user is a staff or not"
        )
    )

    groups = []
    user_permissions = []

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{} <{}>".format(self.full_name(), self.email)

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Always Yes
        :param perm:
        :param obj:
        :return:
        """
        return True 

    def has_module_perms(self, app_label):
        """
        Does the user have the permission to view the app_label?
        Always Yes
        :param app_label:
        :return:
        """
        return True 