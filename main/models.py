from django.db import models


class Category (models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
         self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Hub (models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
         self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Product (models.Model):
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, blank=True)
    hub =  models.ManyToManyField(Hub, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created =  models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
         self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)