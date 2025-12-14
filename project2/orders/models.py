from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from accounts.models import User
from restaurant.models import MenuItem


class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        ("delivery", "Giao hàng"),
        ("pickup", "Lấy tại quán"),
        ("dine_in", "Ăn tại quán"),
    )

    STATUS_CHOICES = (
        ("pending", "Chờ xác nhận"),
        ("confirmed", "Đã xác nhận"),
        ("preparing", "Đang chuẩn bị"),
        ("ready", "Sẵn sàng"),
        ("delivering", "Đang giao"),
        ("completed", "Hoàn thành"),
        ("cancelled", "Đã hủy"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("cod", "Thanh toán khi nhận hàng"),
        ("bank_transfer", "Chuyển khoản ngân hàng"),
        ("momo", "Ví MoMo"),
        ("zalopay", "ZaloPay"),
    )

    PAYMENT_STATUS_CHOICES = (
        ("pending", "Chờ thanh toán"),
        ("paid", "Đã thanh toán"),
        ("refunded", "Đã hoàn tiền"),
    )

    # Order info
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    order_type = models.CharField(
        max_length=20, choices=ORDER_TYPE_CHOICES, default="delivery"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )

    # Delivery info
    delivery_name = models.CharField(
        max_length=100, verbose_name="Tên người nhận"
    )
    delivery_phone = models.CharField(
        max_length=15, verbose_name="SĐT người nhận"
    )
    delivery_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    delivery_note = models.TextField(blank=True, verbose_name="Ghi chú")

    # Pricing
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Tạm tính"
    )
    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Phí vận chuyển",
    )
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Giảm giá"
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Tổng tiền"
    )

    # Payment
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default="cod"
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD + timestamp
            import time

            self.order_number = f"ORD{int(time.time())}"
        super().save(*args, **kwargs)

    def get_status_display_class(self):
        """Trả về class Bootstrap cho status badge"""
        status_classes = {
            "pending": "warning",
            "confirmed": "info",
            "preparing": "primary",
            "ready": "success",
            "delivering": "info",
            "completed": "success",
            "cancelled": "danger",
        }
        return status_classes.get(self.status, "secondary")

    def calculate_total(self):
        """Tính tổng tiền đơn hàng"""
        self.subtotal = sum(
            item.get_total_price() for item in self.items.all()
        )

        # Free shipping cho đơn > 200k
        if self.subtotal >= 200000:
            self.delivery_fee = 0
        else:
            self.delivery_fee = 30000

        self.total_amount = self.subtotal + self.delivery_fee - self.discount
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Đơn giá"
    )
    note = models.TextField(blank=True, verbose_name="Ghi chú món")

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

    def get_total_price(self):
        return self.price * self.quantity


class Coupon(models.Model):
    """Mã giảm giá"""

    code = models.CharField(max_length=50, unique=True, verbose_name="Mã")
    discount_type = models.CharField(
        max_length=20,
        choices=(
            ("percentage", "Phần trăm"),
            ("fixed", "Số tiền cố định"),
        ),
        default="percentage",
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Giá trị giảm"
    )
    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Đơn hàng tối thiểu",
    )
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Giảm tối đa",
    )
    usage_limit = models.IntegerField(
        null=True, blank=True, verbose_name="Giới hạn sử dụng"
    )
    used_count = models.IntegerField(default=0, verbose_name="Đã sử dụng")
    valid_from = models.DateTimeField(verbose_name="Có hiệu lực từ")
    valid_to = models.DateTimeField(verbose_name="Có hiệu lực đến")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    class Meta:
        verbose_name = "Mã giảm giá"
        verbose_name_plural = "Mã giảm giá"

    def __str__(self):
        return self.code

    def is_valid(self):
        """Kiểm tra mã còn hiệu lực không"""
        from django.utils import timezone

        now = timezone.now()

        if not self.is_active:
            return False, "Mã đã hết hiệu lực"

        if now < self.valid_from:
            return False, "Mã chưa có hiệu lực"

        if now > self.valid_to:
            return False, "Mã đã hết hạn"

        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "Mã đã hết lượt sử dụng"

        return True, "Mã hợp lệ"

    def calculate_discount(self, order_amount):
        """Tính số tiền giảm giá"""
        if order_amount < self.min_order_amount:
            return 0

        if self.discount_type == "percentage":
            discount = order_amount * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value

        return discount
