from django.db import models


class Category(models.Model):
    """ Create the default model format for a category """
    class Meta:
        """ Set the plural name """
        verbose_name_plural = 'Categories'

    # Set the model fields
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254,
                                     blank=True)

    def __str__(self):
        """ Return the category name when called """
        return self.name

    def get_friendly_name(self):
        """ Return the category friendly name when called """
        return self.friendly_name


class Product(models.Model):
    """ Create the default model format for a product """
    # Set the model fields
    category = models.ForeignKey('Category', null=True, blank=False,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=False, blank=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                default=7.99)
    image = models.ImageField(null=False, blank=False)

    def __str__(self):
        """ Return the product name when called """
        return self.name
