class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    recipe = models.TextField(blank=True)  # Công thức
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="menu/")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Chef(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to="chefs/")
