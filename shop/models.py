from django.db import models
from products.models import Product
from users.models import Basket
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
######################## Shop Requirments ###############################
class Shop(models.Model):

    name = models.CharField(_("Name"), max_length=200, db_index=True)
    address = models.CharField(_("Address"), max_length=200)
    page = models.CharField(_("Page"), max_length=200)
    # product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='shop', related_query_name='shop')
    product = models.ManyToManyField(Product, verbose_name=_("Product"), related_name='shop', related_query_name='shop')
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
    
    def users_orders(self):
        return Basket.objects.filter(state=True)
    
    def single_user_orders(self, username):
        basket = User.objects.filter(username=username).basket.filter(state=True)
        return basket
    
    def change_user_order(self, username, state):
        User.objects.filter(username=username).basket.update(state=state)
    
    def earns(self):
        baskets_prices = Basket.objects.filter(state=True).product.price
        return baskets_prices
