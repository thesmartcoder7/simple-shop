from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.category_name.title()
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.product_name.title()
    

class VariationType(models.Model):
    variation_name = models.CharField(max_length=50)

    def __str__(self):
        return self.variation_name


class VariationOption(models.Model):
    variation_type = models.ForeignKey(VariationType, on_delete=models.CASCADE, related_name="options")
    option_name = models.CharField(max_length=50)  # e.g., Red, Large, All-Terrain
    price_change = models.DecimalField(decimal_places=2, max_digits=8, default=0)  # Price impact of this option

    def __str__(self):
        return f"{self.option_name} ({self.price_change:+.2f})"
    
    

class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    base_price = models.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        verbose_name_plural = 'Product Items'

    def __str__(self) -> str:
        return f"{self.pk} - {self.product.product_name.title()}"
    

class ProductVariation(models.Model):
    variation_options = models.ManyToManyField(VariationOption)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Product Variations'

    def __str__(self) -> str:
        options = ", ".join([str(option) for option in self.variation_options.all()])
        return f"Options: {options}"
    
    def total_price(self):
        # Calculate the total price: base price + sum of all selected option price changes
        variation_price = sum(option.price_change for option in self.variation_options.all())
        return self.product_item.base_price + variation_price
