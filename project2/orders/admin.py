from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["price", "get_total_price"]

    def get_total_price(self, obj):
        return f"{obj.get_total_price():,.0f}đ"

    get_total_price.short_description = "Thành tiền"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "customer",
        "order_type",
        "status",
        "payment_status",
        "total_amount",
        "created_at",
    ]
    list_filter = ["status", "payment_status", "order_type", "created_at"]
    search_fields = ["order_number", "customer__username", "delivery_phone"]
    readonly_fields = [
        "order_number",
        "subtotal",
        "delivery_fee",
        "discount",
        "total_amount",
        "created_at",
        "updated_at",
    ]
    inlines = [OrderItemInline]

    fieldsets = (
        (
            "Thông tin đơn hàng",
            {"fields": ("order_number", "customer", "order_type", "status")},
        ),
        (
            "Thông tin giao hàng",
            {
                "fields": (
                    "delivery_name",
                    "delivery_phone",
                    "delivery_address",
                    "delivery_note",
                )
            },
        ),
        (
            "Chi tiết giá",
            {
                "fields": (
                    "subtotal",
                    "delivery_fee",
                    "discount",
                    "total_amount",
                )
            },
        ),
        ("Thanh toán", {"fields": ("payment_method", "payment_status")}),
        (
            "Thời gian",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "confirmed_at",
                    "completed_at",
                )
            },
        ),
    )

    actions = ["mark_as_confirmed", "mark_as_completed"]

    def mark_as_confirmed(self, request, queryset):
        from django.utils import timezone

        updated = queryset.filter(status="pending").update(
            status="confirmed", confirmed_at=timezone.now()
        )
        self.message_user(request, f"Đã xác nhận {updated} đơn hàng")

    mark_as_confirmed.short_description = "Xác nhận đơn hàng đã chọn"

    def mark_as_completed(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(
            status="completed", completed_at=timezone.now()
        )
        self.message_user(request, f"Đã hoàn thành {updated} đơn hàng")

    mark_as_completed.short_description = "Đánh dấu hoàn thành"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "discount_type",
        "discount_value",
        "min_order_amount",
        "used_count",
        "usage_limit",
        "is_active",
        "valid_from",
        "valid_to",
    ]
    list_filter = ["discount_type", "is_active", "valid_from", "valid_to"]
    search_fields = ["code"]
