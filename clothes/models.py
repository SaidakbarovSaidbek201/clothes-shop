from django.db import models

# Create your models here.
class Category(models.Model):
    rasmi = models.URLField(max_length=255,default='default_value')
    nomi = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def __str__(self):
        return self.nomi
    
    def save(self, *args, **kwargs):
        self.slug = self.nomi.lower().replace(' ', '-')
        super(Category, self).save(*args, **kwargs)
    

class Clothes(models.Model):
    nomi = models.CharField(max_length=250)
    rasmi = models.URLField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    describtion = models.CharField(max_length=500)
    prize = models.IntegerField()

    def __str__(self):
        return self.nomi
    
class Cart(models.Model):
    def add_product(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

    def remove_product(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"
    