from django.db import models

class BaseModel(models.Model):
    slug = models.SlugField(max_length=200, blank=True)
    name = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
         self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)


class Category(BaseModel):
    name = models.CharField(max_length=45)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"])
        ]

class Hub(BaseModel):
    name = models.CharField(max_length=45)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"])
        ]
    

class Product(BaseModel):
    category = models.ManyToManyField(Category, blank=True)
    hub =  models.ManyToManyField(Hub, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)