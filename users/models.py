from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


# Create your models here.

######## User Manger #################
class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        try:
            return self.get(username=username)
        except self.model.DoesNotExist:
            return self.get(is_active=True, email=username)


######### User ###########################
class User(AbstractUser):
    objects = UserManager()

    username = models.CharField(_("Userame"), max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    native_name = models.CharField(_("Native Name"), max_length=50)
    phone_no = models.CharField(_("Phone Number"), max_length=10)
    image = models.ImageField(_("Profile Picture"), upload_to="users", height_field=None, width_field=None, max_length=None)
    # password = models.CharField(_("Password Field"), max_length=50, required=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'email'] 

    
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        swappable = 'AUTH_USER_MODEL'
    

    def get_username(self):
        return self.email
    

    def __str__(self):
        if self.is_staff or self.is_superuser:
            return self.username
        else:
            return self.email or '<anonymose>'
    

    def get_full_name(self):
        full_name = super(User,self).get_full_name()

        if full_name:
            return full_name
        return self.get_short_name()
    

    def get_short_name(self):
        short_name = super(User, self).get_short_name()
        
        if short_name:
            return short_name
        return self.email
    

    def validate_unique(self, exclude=None):
        super(User, self).validate_unique(exclude)
        if self.email and get_user_model().objects.exclude(id=self.id).filter(is_active=True,
                                                                              email__exact=self.email).exists():
            msg = _("A customer with the e-mail address `{email}` already exists.")
            raise ValidationError({'email': msg.format(email=self.email)})


######### Address model for users
class Address(models.Model):

    province = models.CharField(_("Province"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    street = models.CharField(_("Street"), max_length=50)
    lane = models.CharField(_("Lane"), max_length=50)
    postal_code = models.CharField(_("Postal Code"), max_length=50)
    fk = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='user_address', related_query_name='user_address')
    slug = models.SlugField(_("Slug"))
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.postal_code

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})


