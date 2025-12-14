from django.core.management.base import BaseCommand
from restaurant.models import Category, MenuItem, Chef
from decimal import Decimal


class Command(BaseCommand):
    help = "Tạo dữ liệu mẫu cho restaurant"

    def handle(self, *args, **kwargs):
        # Tạo Categories
        categories_data = [
            {"name": "Khai vị", "description": "Các món khai vị ngon miệng"},
            {"name": "Món chính", "description": "Các món chính đặc sắc"},
            {
                "name": "Tráng miệng",
                "description": "Các món tráng miệng hấp dẫn",
            },
            {"name": "Đồ uống", "description": "Các loại nước giải khát"},
            {"name": "Món chay", "description": "Các món ăn chay dinh dưỡng"},
        ]

        for cat_data in categories_data:
            Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={"description": cat_data["description"]},
            )

        self.stdout.write(self.style.SUCCESS("Created categories"))

        # Tạo Menu Items
        appetizer = Category.objects.get(name="Khai vị")
        main = Category.objects.get(name="Món chính")

        menu_items_data = [
            {
                "name": "Gỏi cuốn tôm thịt",
                "category": appetizer,
                "description": "Gỏi cuốn tươi ngon với tôm và thịt heo",
                "price": Decimal("50000"),
                "is_featured": True,
            },
            {
                "name": "Phở bò",
                "category": main,
                "description": "Phở bò truyền thống Hà Nội",
                "price": Decimal("70000"),
                "discount_price": Decimal("60000"),
                "is_featured": True,
            },
            {
                "name": "Bún chả Hà Nội",
                "category": main,
                "description": "Bún chả đặc sản Hà Nội",
                "price": Decimal("65000"),
                "is_featured": True,
            },
        ]

        for item_data in menu_items_data:
            MenuItem.objects.get_or_create(
                name=item_data["name"], defaults=item_data
            )

        self.stdout.write(self.style.SUCCESS("Created menu items"))

        # Tạo Chefs
        chefs_data = [
            {
                "name": "Nguyễn Văn A",
                "position": "Head Chef",
                "bio": "Với hơn 15 năm kinh nghiệm trong nghề",
                "specialization": "Món Việt truyền thống",
            },
            {
                "name": "Trần Thị B",
                "position": "Sous Chef",
                "bio": "Chuyên gia về các món tráng miệng",
                "specialization": "Pastry & Dessert",
            },
        ]

        for chef_data in chefs_data:
            Chef.objects.get_or_create(
                name=chef_data["name"], defaults=chef_data
            )

        self.stdout.write(self.style.SUCCESS("Created chefs"))
        self.stdout.write(
            self.style.SUCCESS("Sample data created successfully!")
        )
