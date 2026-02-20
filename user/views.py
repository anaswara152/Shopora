from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,get_user_model
from django.contrib.auth.models import User,Group
from django.contrib import messages
from .models import*
from siteadmin.models import*
import uuid



# Create your views here.
def home(request):
    return render(request,'common/home.html')


def registration(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        city=request.POST['city']
        postalcode=request.POST['postalcode']
        state=request.POST['state']
        password=request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.info(request,'email existing')
            return render(request,'user/register.html')
        elif User.objects.filter(username=email).exists():
             messages.info(request,'email not existing')
             return render(request,'user/register.html')
        else:
            user=User.objects.create_user(username=username, first_name= first_name,last_name=last_name,email=email,password=password)
            user.save()
            customer=reg(user=user,address=address,city=city,state=state,postalcode=postalcode,phone=phone)
            customer.save()
            messages.success(request,'Registration successfull..')
            customer_obj,created=Group.objects.get_or_create(name="CUSTOMER")
            customer_obj.user_set.add(user)
            return redirect('registration')

    return render(request,'user/register.html')


from django.db.models import Q

def userhome(request):
    
    products = Product.objects.all()
    categories = category.objects.all()

    search = request.GET.get('search')
    categorys = request.GET.get('category')
    color = request.GET.get('color')
    size = request.GET.get('size')
    gender = request.GET.get('gender')

    is_filtered = False

    if search:
        products = products.filter(name__icontains=search)
        is_filtered = True

    if categorys:
        products = products.filter(categoryid__id=categorys)
        is_filtered = True


    if size:
        products = products.filter(size__icontains=size)
        is_filtered = True


    if request.user.is_authenticated:
        user_wishlist_ids = whislist.objects.filter(
            customerid=request.user
        ).values_list('productid_id', flat=True)
    else:
        user_wishlist_ids = []

    return render(request, 'user/userhome.html', {
        'm': products,
        'categories': categories,
        'user_wishlist_ids': user_wishlist_ids,
        'is_filtered': is_filtered
    })
    
def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('userhome')
        else:
            return redirect('adminhome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('userhome')
            else:
                return redirect('adminhome')
        else:
            messages.error(request, 'User credentials are not correct')

    return render(request, 'common/login.html')

def logoutuser(request):
     if request.user.is_authenticated:
           request.session.flush()
     return redirect('home')

def deatiles(request,id):
    m=Product.objects.filter(id=id)
    p={'m':m}
    return render(request,'user/showdetails.html',p) 

def addcart(request):
    if request.user.is_authenticated:

        product_id = request.POST['productid']
        count = int(request.POST['count'])

        product = Product.objects.get(id=product_id)

        if product.stock_quantity == 0:
            messages.error(request, "Out of Stock")
            return redirect('userhome')

        if count > product.stock_quantity:
            messages.error(request, "Only limited stock available")
            return redirect('userhome')

        price = product.base_price

        cart.objects.create(
            customerid_id=request.user.id,
            productid_id=product.id,
            count=count,
            price=price
        )

        product.stock_quantity -= count
        product.save()

        messages.success(request, "Added to cart")

    return redirect('userhome')

def viewcart(request):
    id = request.user.id
    cart_obj = cart.objects.filter(customerid_id=id)

    grand = 0

    for c in cart_obj:
        c.total = c.count * c.price  
        grand += c.total

    p = {'n': cart_obj, 'gr': grand}
    return render(request, 'user/viewcart.html', p)

def deletecart(request,id): 
    m=cart.objects.filter(id=id).delete()
    return redirect('viewcart')  

def trash(request,id):
    productid=cart.objects.filter(id=id)
    customerid=request.user.id
    number=productid[0].count
    if number==0:
        messages.info('blank')
        return redirect('viewcart')
    else:
        quantity=number-1
        p=productid.update(count=quantity)
        return redirect('viewcart')
    
def addproduct(request,id):
    productid=cart.objects.filter(id=id)
    customerid=request.user.id
    num=productid[0].count
    if num==0:
        messages.info(request,'blank')
        return redirect('viewcart')
    else:
        qunt=num+1
        k=productid.update(count=qunt)
        return redirect('viewcart')
    
def deletecart(request,id): 
    m=cart.objects.filter(id=id).delete()
    return redirect('viewcart')    
def addwhis(request, id):
    if not request.user.is_authenticated:
        return redirect('loginuser')

    product_instance = get_object_or_404(Product, id=id)

    exists = whislist.objects.filter(productid=product_instance, customerid=request.user).exists()

    if not exists:
        whislist.objects.create(productid=product_instance, customerid=request.user)
        messages.success(request, "Item added to your wishlist ❤️")
    else:
        messages.info(request, "This item is already in your wishlist 💖")

    return redirect('userhome')


def toggle_wishlist(request, id):
    product_instance = get_object_or_404(Product, id=id)

    user = request.user

    wishlist_item = whislist.objects.filter(productid=product_instance, customerid=user)

    if wishlist_item.exists():
        wishlist_item.delete()
    else:
        whislist.objects.create(productid=product_instance, customerid=user)

    return redirect('userhome')



def viewwish(request):
    id=request.user.id
    wish_obj=whislist.objects.filter(customerid_id=id)
 
    return render(request,'user/viewish.html',{'w':wish_obj})


def removewish(request, wish_id):
    wish_item = get_object_or_404(whislist, id=wish_id, customerid=request.user)
    wish_item.delete()
    messages.success(request, "Removed from wishlist")
    return redirect('viewwish')


def payment_page(request):
    if request.method == "POST":
        product_ids = request.POST.getlist('productid')
        quantities = request.POST.getlist('count')   

        cart_items = []
        grand_total = 0

        for pid, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=pid)
            qty = int(qty)
            total = product.base_price * qty
            grand_total += total

            cart_items.append({
                'product': product,
                'quantity': qty,
                'total': total
            })

        return render(request, 'user/payment.html', {
            'cart_items': cart_items,
            'grand_total': grand_total
        })

    return redirect('viewcart')

def place_order(request):
    if request.method == "POST":

        product_id = request.POST['productid']
        quantity = int(request.POST['quantity'])
        payment_method = request.POST.get('payment_method')

        product = get_object_or_404(Product, id=product_id)

        if product.stock_quantity < quantity:
            messages.error(request, "Not enough stock")
            return redirect('userhome')

        total = product.base_price * quantity
        Order.objects.create(
            customer=request.user,
            product=product,
            quantity=quantity,
            total_price=total,
            payment_method=payment_method
        )

        product.stock_quantity -= quantity
        product.save()

        messages.success(request, "Order Placed Successfully!")

        return redirect('userhome')

    return redirect('userhome')

def process_payment(request):
    if request.method == "POST":

        product_ids = request.POST.getlist('productid')
        quantities = request.POST.getlist('quantity')
        payment_method = request.POST.get('payment_method')

        products_data = []
        grand_total = 0

        for pid, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=pid)
            qty = int(qty)
            total = product.base_price * qty
            grand_total += total

            products_data.append({
                'product': product,
                'quantity': qty,
                'total': total
            })

        if payment_method == "COD":

            order = Order.objects.create(
                customer=request.user,
                total_price=grand_total,
                payment_method="COD",
                payment_status="PENDING",
                order_status="PENDING"
            )

            for item in products_data:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['total']
                )

                item['product'].stock_quantity -= item['quantity']
                item['product'].save()

            cart.objects.filter(customerid=request.user).delete()

            messages.success(request, "Order placed successfully with Cash On Delivery!")
            return redirect('cod_success', order_id=order.id)

        return render(request, 'user/payment_details.html', {
            'products': products_data,
            'payment_method': payment_method,
            'grand_total': grand_total
        })

    return redirect('viewcart')





def save_order(request, product, quantity, total, payment_method):

    if product.stock_quantity < quantity:
        messages.error(request, "Not enough stock")
        return redirect('userhome')

    transaction_id = str(uuid.uuid4())[:12]

    if payment_method == "COD":
        payment_status = "PENDING"
    else:
        payment_status = "PAID"

    Order.objects.create(
        customer=request.user,
        product=product,
        quantity=quantity,
        total_price=total,
        payment_method=payment_method,
        payment_status=payment_status,
        transaction_id=transaction_id
    )

    product.stock_quantity -= quantity
    product.save()

    messages.success(request, "Order Placed Successfully!")

    return redirect('userhome')

def complete_online_payment(request):
    if request.method == "POST":

        product_ids = request.POST.getlist('productid')
        quantities = request.POST.getlist('quantity')
        payment_method = request.POST.get('payment_method')

        total_amount = 0

        for pid, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=pid)
            total_amount += product.base_price * int(qty)

        order = Order.objects.create(
            customer=request.user,
            total_price=total_amount,
            payment_method=payment_method,
            payment_status='PAID'
        )

        for pid, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=pid)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(qty),
                price=product.base_price * int(qty)
            )

        cart.objects.filter(customerid=request.user).delete()

        return redirect('payment_success', order_id=order.id)

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'user/payment_success.html', {'order': order})

def cod_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'user/cod_success.html', {'order': order})


def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'user/my_orders.html', {'orders': orders})



def my_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'user/my_order_details.html', {'order': order})


def user_cancel_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, customer=request.user)

        if order.order_status in ['PENDING', 'PROCESSING']:
            order.order_status = 'CANCELLED'
            order.save()

            for item in order.items.all():
                product = item.product
                product.stock_quantity += item.quantity
                product.save()

            messages.success(request, f"Order #{order.id} has been cancelled successfully!")
        else:
            messages.error(request, "Cannot cancel a completed or already cancelled order.")

    return redirect('my_orders')



def view_profile(request):
    profile = get_object_or_404(reg, user=request.user)
    return render(request, 'user/view_profile.html', {'profile': profile})


def edit_profile(request):
    profile = get_object_or_404(reg, user=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.postalcode = request.POST.get('postalcode')
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('view_profile')

    return render(request, 'user/edit_profile.html', {'profile': profile})


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('forgot_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please login.")
            return redirect('login_user')
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('forgot_password')

    return render(request, 'user/forgot_password.html')



