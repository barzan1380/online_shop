from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    off = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def get_absolute_url(self):
        return reverse('shop:products_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    # مدل ایجاد محصول
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=2000)
    inventory = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    discount_start = models.DateTimeField(blank=True, null=True) #تاریخ شروع تخفیف
    discount_end = models.DateTimeField(blank=True, null=True)  # تاریخ پایان تخفیف
    off = models.PositiveIntegerField(default=0) #مقدار درصدی تخفیف
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])

    def get_final_discount_percent(self):
        return max(self.off, self.category.off)

    def is_discount_active(self):
        now = timezone.now()
        return self.discount_start and self.discount_end and self.discount_start<= now <= self.discount_end

    def get_final_price(self):
        if self.is_discount_active():
            off_amount = (self.get_final_discount_percent() / 100) * self.price
            return int(self.price - off_amount)
        return self.price

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='تصویرها'),
    title = models.CharField(max_length=50),
    file = models.ImageField(upload_to='product_image/%Y/%m/%d'),
    description = models.TextField(max_length=2000),
    create = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create'])
        ]

    def __str__(self):
        return self.title if self.title else 'None'


class ProductFeature(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')

    def __str__(self):
        return self.name + self.value
