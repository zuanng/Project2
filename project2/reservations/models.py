class Table(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)


class Reservation(models.Model):
    STATUS_CHOICES = (
        ("pending", "Chờ xác nhận"),
        ("confirmed", "Đã xác nhận"),
        ("completed", "Hoàn thành"),
        ("cancelled", "Đã hủy"),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
