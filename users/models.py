from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from products.models import Product


# Create your models here.

######## User Manger #################
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


######### User ###########################
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()
    
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True
    )

    email = models.EmailField(_('email address'),
        help_text=_('Enter a valid email address'),
        validators=[email_validator],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
        unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('User')
        swappable = 'AUTH_USER_MODEL'
    

    def get_username(self):
        return self.email
    

    def __str__(self):
        if self.is_staff or self.is_superuser:
            return self.username
        else:
            return self.email or '<anonymose>'
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # def get_full_name(self):
    #     """
    #     Return the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()
    

    # def get_short_name(self):
    #     """Return the short name for the user."""
    #     return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def validate_unique(self, exclude=None):
        super(User, self).validate_unique(exclude)
        if self.email and get_user_model().objects.exclude(id=self.id).filter(is_active=True,
                                                                              email__exact=self.email).exists():
            msg = _("A customer with the e-mail address `{email}` already exists.")
            raise ValidationError({'email': msg.format(email=self.email)})


############################### Profile ######################################
class Profile(models.Model):
    User = get_user_model()

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    avatar = models.ImageField(_("avatar"), upload_to='user/avatars', blank=True, )
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, db_index=True, related_name='profile', related_query_name='profile')

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Profile_detail", kwargs={"pk": self.pk})
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


######### Address model for users ##################
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


###################### Comments of user ################################
class Comment(models.Model):

    User = get_user_model()
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name='comment', related_query_name='comment')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='comment', related_query_name='comment')
    title = models.CharField(_("Title"), max_length=150)
    body = models.TextField(_("Body"))
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)
    publish = models.DateTimeField(_("Publish"), default=timezone.now)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Comments_detail", kwargs={"pk": self.pk})
    
    @property
    def count_like(self):
        likes = self.like.all()
        return likes.count()


##################### Likes ###################################
class ProductLike(models.Model):

    User = get_user_model()

    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name='product_like', related_query_name='product_like')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='like', related_query_name='like')
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)

    class Meta:
        unique_together = [['author', 'product']]
        verbose_name = _("ProductLike")
        verbose_name_plural = _("ProductLikes")

    def __str__(self):
        return self.author


class CommentLike(models.Model):

    User = get_user_model()

    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name='comment_like', related_query_name='comment_like')
    comment = models.ForeignKey(Comment, verbose_name=_("Comment"), on_delete=models.CASCADE, related_name='like', related_query_name='like')
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")
        unique_together = [['author', 'comment']]

    def __str__(self):
        return self.author

###############################  Available and non avaiable products for users ##################################
class AvailableProductForUser(models.Model):

    User = get_user_model()

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='available_product')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("AvailableProductForUser")
        verbose_name_plural = _("AvailableProductForUsers")

    def __str__(self):
        return self.user


    def available_products(self):
        products = Product.objects.filter(available=True)
        return products
    
    def non_availabl_products(self):
        products = Product.objects.filter(available=False)
        return products


################################ User Basket ##############################
class Basket(models.Model):

    User = get_user_model()
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='basket', related_query_name='basket')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='basket', related_query_name='basket')
    state = models.BooleanField(_("State"), default=False)
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Basker_detail", kwargs={"pk": self.pk})

    def prev_transactions(self):
        prev = self.objects.filter(state=True)
        return prev