from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


# Create your models here.

####################### Product Requirments ############################
class Category(models.Model):

    name = models.CharField(_("Name"), max_length=200, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)

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

    class Meta:
        ordering = ('name',)
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Brand_detail", kwargs={"pk": self.pk})



class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE, related_name='products', related_query_name='products')
    brand = models.ForeignKey(Brand, verbose_name=_("Brand"), on_delete=models.CASCADE, related_name='products', related_query_name='products')
    name = models.CharField(_("Name"), max_length=200, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, db_index=True)
    image = models.ImageField(_("Image"), upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    available = models.BooleanField(_("Available"), default=True)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    # What is tag?


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})



class ProductView(models.Model):

    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='views', related_query_name='views')
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("ProductView")
        verbose_name_plural = _("ProductViews")

    def __str__(self):
        return self.product

    def get_absolute_url(self):
        return reverse("ProductView_detail", kwargs={"pk": self.pk})



######################## Shop Requirments ###############################
class Shop(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    address = models.CharField(_("Address"), max_length=200)
    page = models.CharField(_("Page"), max_length=200)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='shop', related_query_name='shop')

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Shop_detail", kwargs={"pk": self.pk})
    

    def make_product_available(self, product_id, available=True):
        Product.objects.filter(id=product_id).update(Product__available=available)
    

    def set_price_of_product(self, product_id, price):
        Product.objects.filter(id=product_id).update(Product__price=price)
