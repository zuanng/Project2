from django import forms
from .models import Order, OrderItem, Coupon
from django.utils import timezone


class CheckoutForm(forms.ModelForm):
    """Form checkout đơn hàng"""

    coupon_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nhập mã giảm giá"}
        ),
    )

    class Meta:
        model = Order
        fields = [
            "order_type",
            "delivery_name",
            "delivery_phone",
            "delivery_address",
            "delivery_note",
            "payment_method",
        ]
        widgets = {
            "order_type": forms.Select(attrs={"class": "form-select"}),
            "delivery_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Họ và tên"}
            ),
            "delivery_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Số điện thoại"}
            ),
            "delivery_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Địa chỉ chi tiết",
                }
            ),
            "delivery_note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Ghi chú cho đơn hàng (tùy chọn)",
                }
            ),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Pre-fill user information
        if user and user.is_authenticated:
            self.fields["delivery_name"].initial = user.get_full_name()
            self.fields["delivery_phone"].initial = user.phone
            if hasattr(user, "customer_profile"):
                self.fields["delivery_address"].initial = (
                    user.customer_profile.address
                )


class OrderItemNoteForm(forms.ModelForm):
    """Form thêm ghi chú cho món ăn"""

    class Meta:
        model = OrderItem
        fields = ["note"]
        widgets = {
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Ví dụ: Không hành, thêm ớt...",
                }
            )
        }
