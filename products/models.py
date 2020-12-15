from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


# Create your models here.

####################### Product Requirments ############################
class Category(models.Model):

    name = models.CharField(_("Name"), max_length=200, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    parent = models.ForeignKey("self", verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True, related_query_name='child', related_name='child')
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})



class Brand(models.Model):

    name = models.CharField(_("Name"), max_length=50, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Brand_detail", kwargs={"pk": self.pk})


class ImageGallery(models.Model):

    image = models.ImageField(_("Image"), upload_to='products/%Y/%m/%d', blank=True)
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE, related_name='image', related_query_name='image')
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)   

    class Meta:
        verbose_name = _("ImageGallery")
        verbose_name_plural = _("ImageGalleries")

    def __str__(self):
        return self.product




class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE, related_name='product', related_query_name='product')
    brand = models.ForeignKey(Brand, verbose_name=_("Brand"), on_delete=models.CASCADE, related_name='product', related_query_name='product')
    name = models.CharField(_("Name"), max_length=200, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, db_index=True)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    available = models.BooleanField(_("Available"), default=True)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    sold = models.BooleanField(_("Sold"), default=False)
    view = models.IntegerField(_("View"), default=0)
    # What is tag?


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})
    
    def count_like(self):
        likes = self.like.all()
        return likes.count()
    
    def count_sells(self):
        return self.objects.filter(sold=True)
    
    def count_views(self):
        return self.objects.all().count()



# class ProductView(models.Model):

#     product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='views', related_query_name='views')
#     created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
#     updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

#     class Meta:
#         verbose_name = _("ProductView")
#         verbose_name_plural = _("ProductViews")

#     def __str__(self):
#         return self.product

