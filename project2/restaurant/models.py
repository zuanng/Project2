from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    order = models.IntegerField(default=0, verbose_name="Thứ tự")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "restaurant:category_detail", kwargs={"slug": self.slug}
        )


class MenuItem(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên món")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="Danh mục",
    )
    description = models.TextField(verbose_name="Mô tả")
    recipe = models.TextField(blank=True, verbose_name="Công thức")
    ingredients = models.TextField(blank=True, verbose_name="Nguyên liệu")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Giá"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Giá khuyến mãi",
    )
    image = models.ImageField(upload_to="menu/", verbose_name="Ảnh")
    is_available = models.BooleanField(default=True, verbose_name="Còn hàng")
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    is_vegetarian = models.BooleanField(default=False, verbose_name="Chay")
    is_spicy = models.BooleanField(default=False, verbose_name="Cay")
    preparation_time = models.IntegerField(
        default=15, verbose_name="Thời gian chuẩn bị (phút)"
    )
    views_count = models.IntegerField(default=0, verbose_name="Lượt xem")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Món ăn"
        verbose_name_plural = "Món ăn"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("restaurant:menu_detail", kwargs={"slug": self.slug})

    @property
    def get_price(self):
        """Trả về giá hiện tại (có khuyến mãi thì lấy giá KM)"""
        if self.discount_price:
            return self.discount_price
        return self.price

    @property
    def discount_percentage(self):
        """Tính % giảm giá"""
        if self.discount_price and self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0


class MenuItemImage(models.Model):
    """Ảnh phụ cho món ăn"""

    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="menu/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.menu_item.name}"


class Chef(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên")
    slug = models.SlugField(unique=True)
    position = models.CharField(max_length=100, verbose_name="Chức vụ")
    bio = models.TextField(verbose_name="Tiểu sử")
    specialization = models.CharField(
        max_length=200, blank=True, verbose_name="Chuyên môn"
    )
    image = models.ImageField(upload_to="chefs/", verbose_name="Ảnh")
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Đang làm việc")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Đầu bếp"
        verbose_name_plural = "Đầu bếp"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.position}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Review(models.Model):
    """Đánh giá món ăn"""

    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ["-created_at"]
        unique_together = ["menu_item", "user"]

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name} ({self.rating}★)"
