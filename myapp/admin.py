from django.contrib import admin
from .models import*
from myapp.models import Order
from django.utils.safestring import mark_safe
import json
# Register your models here.

admin.site.site_header="Monginis Admin Panel"
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    readonly_fields = ("formatted_cart_items",)

    def formatted_cart_items(self, obj):
        items = json.dumps(obj.cart_items, indent=2)  # Format JSON nicely
        return mark_safe(f"<pre>{items}</pre>")


admin.site.register(Registration)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderCartItem)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Cake)
admin.site.register(Pastry)
admin.site.register(Packaged_cake)
admin.site.register(Brownie)
admin.site.register(Chocolate)
admin.site.register(Donut)
admin.site.register(Muffin)
admin.site.register(Chocolate_bouquet)
admin.site.register(NewArrivals)
admin.site.register(OrderCart)
admin.site.register(Profile)