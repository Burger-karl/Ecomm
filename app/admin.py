# from django.contrib import admin
# from .models import Cart, OrderPlaced, Payment, Product, Customer, Wishlist
# from django.utils.html import format_html
# from django.urls import reverse
# from django.contrib.auth.models import Group

# # Register your models here.

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ['id','title','discounted_price','category','product_image']


# @admin.register(Customer)
# class CustomerModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','locality','city','state','zipcode']
    

# @admin.register(Cart)
# class CartModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','products','quantity']
#     def products(self,obj):
#         link = reverse("admin:app_product_change",args=[obj.product.pk])
#         return format_html('<a href="{}">{}</a>',link, obj.product.title)


# @admin.register(Payment)
# class PaymentModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']


# @admin.register(OrderPlaced)
# class OrderPlacedModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','customers','products','quantity','ordered_date','status','payments']
#     def customers(self,obj):
#         link = reverse("admin:app_customer_change",args=[obj.customer.pk])
#         return format_html('<a href="{}">{}</a>',link, obj.customer.name)
    
#     def products(self,obj):
#         link = reverse("admin:app_product_change",args=[obj.product.pk])
#         return format_html('<a href="{}">{}</a>',link, obj.product.title)

#     def payments(self,obj):
#         link = reverse("admin:app_payment_change",args=[obj.payment.pk])
#         return format_html('<a href="{}">{}</a>',link, obj.payment.razorpay_payment_id)


# @admin.register(Wishlist)
# class WishlistModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','products']
#     def products(self,obj):
#         link = reverse("admin:app_product_change",args=[obj.product.pk])
#         return format_html('<a href="{}">{}</a>',link, obj.product.title)


# admin.site.unregister(Group)



from django.contrib import admin
from .models import Cart, OrderPlaced, Payment, Product, Customer, Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']
    

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products', 'quantity']

    def products(self, obj):
        link = reverse("admin:ecomm_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'ref', 'email', 'verified', 'date_created']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customers', 'products', 'quantity', 'ordered_date', 'status', 'order_code', 'payments']

    def customers(self, obj):
        link = reverse("admin:ecomm_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    def products(self, obj):
        link = reverse("admin:ecomm_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    def payments(self, obj):
        link = reverse("admin:ecomm_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', link, obj.payment.ref)


@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products']

    def products(self, obj):
        link = reverse("admin:ecomm_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


admin.site.unregister(Group)
