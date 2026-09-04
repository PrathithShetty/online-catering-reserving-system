from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Occasion category e.g. Wedding, Birthday, Corporate Event."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    class FoodType(models.TextChoices):
        STARTER = 'STARTER', 'Starter'
        MAIN_COURSE = 'MAIN', 'Main Course'
        DESSERT = 'DESSERT', 'Dessert'
        BEVERAGE = 'BEVERAGE', 'Beverage'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    food_type = models.CharField(max_length=10, choices=FoodType.choices, default=FoodType.MAIN_COURSE)
    is_veg = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    section = models.CharField(
        max_length=60, blank=True,
        help_text='À la carte menu section, e.g. "Dosa Varieties" — used to group the public Menu page.',
    )

    class Meta:
        ordering = ['section', 'food_type', 'name']

    def __str__(self):
        return self.name


class CateringPackage(models.Model):
    category = models.ForeignKey(Category, related_name='packages', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    price_per_plate = models.DecimalField(max_digits=8, decimal_places=2)
    min_guests = models.PositiveIntegerField(default=20)
    max_guests = models.PositiveIntegerField(default=500)
    menu_items = models.ManyToManyField(MenuItem, related_name='packages', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while CateringPackage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base_slug}-{n}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catering:package_detail', kwargs={'slug': self.slug})

    @property
    def average_rating(self):
        agg = self.reviews.aggregate(avg=models.Avg('rating'))
        return round(agg['avg'], 1) if agg['avg'] else None

    def __str__(self):
        return self.name
