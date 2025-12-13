class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Chờ xác nhận"),
        ("confirmed", "Đã xác nhận"),
        ("preparing", "Đang chuẩn bị"),
        ("delivering", "Đang giao"),
        ("completed", "Hoàn thành"),
        ("cancelled", "Đã hủy"),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
