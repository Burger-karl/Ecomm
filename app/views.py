from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from .models import Cart, Customer, OrderPlaced, Product, Wishlist, Payment
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import uuid
from .paystack_client import PaystackClient

# Create your views here.

paystack_client = PaystackClient()

@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/home.html',locals())

@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about.html',locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contact.html',locals())


@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())


@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title').annotate(total=Count('title'))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/category.html', locals())


@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))        
        
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', locals())



class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! User Register Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/customerregistration.html', locals())


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Profile Saved Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/profile.html', locals())


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())


@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))       
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Congratulations! Profile Update Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return redirect('address')


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html',locals())


def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html',locals())



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()  
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message': 'Wishlist Removed Successfully',
        }
        return JsonResponse(data)


@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'app/search.html', locals())    



@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40  # Add shipping cost

        context = {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount,
        }

        return render(request, 'app/checkout.html', context)
    
    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        customer_id = request.POST.get('custid')
        customer = get_object_or_404(Customer, id=customer_id)

        if not cart_items.exists():
            messages.error(request, 'No items in cart to place an order.')
            return redirect('checkout')  # Redirect back if no items in cart

        total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items) + 40  # Including shipping
        order = OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=cart_items[0].product,  # Assuming one product for simplicity
            quantity=cart_items[0].quantity,
            status='Pending',
            total_amount=total_amount
        )

        # Clear the cart after creating the order
        cart_items.delete()

        # Initiate payment process
        amount = int(order.total_amount * 100)  # Paystack expects amount in kobo
        email = user.email
        order_code = str(uuid.uuid4())

        order.order_code = order_code
        order.save()

        callback_url = request.build_absolute_uri(reverse('verify_payment', kwargs={'ref': order_code}))

        response = paystack_client.initialize_transaction(email, amount, order_code, callback_url)

        if response['status']:
            return redirect(response['data']['authorization_url'])
        else:
            order.order_code = None
            order.save()
            messages.error(request, 'Payment initialization failed.')
            return redirect('checkout')
        

@login_required
def orders(request):
    user = request.user
    order_placed = OrderPlaced.objects.filter(user=user)
    totalitem = len(Cart.objects.filter(user=user))
    wishitem = len(Wishlist.objects.filter(user=user))

    return render(request, 'app/orders.html', {'order_placed': order_placed, 'totalitem': totalitem, 'wishitem': wishitem})


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    user = request.user

    if order.payment_completed:
        messages.error(request, 'Payment already completed for this order.')
        return redirect('orders')

    amount = int(order.total_amount * 100)  # Paystack expects amount in kobo
    email = user.email
    order_code = str(uuid.uuid4())

    order.order_code = order_code
    order.save()

    callback_url = request.build_absolute_uri(reverse('verify_payment', kwargs={'ref': order_code}))

    response = paystack_client.initialize_transaction(email, amount, order_code, callback_url)

    if response['status']:
        return redirect(response['data']['authorization_url'])
    else:
        order.order_code = None
        order.save()
        messages.error(request, 'Payment initialization failed.')
        return redirect('orders')


@login_required
def verify_payment_view(request, ref):
    response = paystack_client.verify_transaction(ref)

    if response['status'] and response['data']['status'] == 'success':
        order = get_object_or_404(OrderPlaced, order_code=ref)
        order.payment_completed = True
        order.status = 'Completed'  # Update order status
        order.save()

        Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.total_amount,
            ref=ref,
            email=request.user.email,
            verified=True
        )

        messages.success(request, 'Payment successful')
        return redirect('orders')
    else:
        messages.error(request, 'Payment verification failed.')
        return redirect('orders')
