from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from user.models import*
# Create your views here.
def adminhome(request):
    return render(request,'admin/adminhome.html')


def productadd(request):
     if request.method =='POST':
         name=request.POST['name']
         size=request.POST['size']
         fabric=request.POST['fabric']
         description=request.POST['description']
         base_price=request.POST['base_price']
         stock_quantity=request.POST['stock_quantity']
         categoryid=request.POST['categoryid']
         if len(request.FILES)>0:
              imge=request.FILES['image']
         else:
              imge='no image'    
         n=Product.objects.create(name=name,size=size,description=description,base_price=base_price,stock_quantity=stock_quantity,categoryid_id=categoryid,fabric=fabric,image=imge)
         n.save()
         messages.info(request,'product added')
     cate=category.objects.all()
     return render(request,'admin/addproduct.html',{'ca':cate})   

def viewproduct(request):
      n=Product.objects.all()
      p={'n':n}
      return render(request,'admin/productshow.html',p) 


def productedit(request,id):
     r=get_object_or_404(Product,id=id)
     if request.method == 'POST':
         name=request.POST['name']
         size=request.POST['size']
         description=request.POST['description']
         base_price=request.POST['base_price']
         stock_quantity=request.POST['stock_quantity']
         categoryid=request.POST['categoryid']
         fabric=request.POST['fabric']
         if 'image' in request.FILES:
            r.image = request.FILES['image']
          
         r.name=name
         r.size=size
         r.fabric=fabric
         r.description=description
         r.base_price=base_price
         r.stock_quantity=stock_quantity
         r.categoryid_id=categoryid
         r.save()
         messages.info(request,'updated')
         return redirect('viewproduct')
     cate=category.objects.all()
     n=Product.objects.filter(id=id)
     return render(request,'admin/editproduct.html',{'ca':cate,'s':n})

def deleteproduct(request,id):
     Product.objects.filter(id=id).delete()
     return redirect('viewproduct')
 
 
def adminview(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/adminview.html', {'orders': orders})

def detailsshow(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == "POST":

        if "start_processing" in request.POST:
            order.carrier = request.POST.get('carrier')
            order.tracking = request.POST.get('tracking_id')
            order.shipping_date = request.POST.get('shipping_date')
            order.order_status = 'PROCESSING'
            order.save()
            return redirect('processing_orders')

        if "cancel_order" in request.POST:
            order.order_status = 'CANCELLED'
            order.payment_status = 'FAILED'
            order.save()
            return redirect('adminview')

    return render(request, 'admin/showdetails.html', {'order': order})

def processing_orders(request):
    orders = Order.objects.filter(order_status='PROCESSING')
    return redirect('admin_orders')

def complete_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.order_status = 'COMPLETED'
    order.payment_status='COMPLETED'
    order.save()
    return redirect('admin_orders')

def cancel_processing(request, id):
    order = get_object_or_404(Order, id=id)
    order.order_status = 'CANCELLED'
    order.payment_status = 'FAILED'
    order.save()
    return redirect('admin_orders')



def admin_orders(request):
    status = request.GET.get('status')  # Read filter from URL

    if status == "pending":
        orders = Order.objects.filter(order_status='PENDING')
        title = "Pending Orders"
    elif status == "processing":
        orders = Order.objects.filter(order_status='PROCESSING')
        title = "Processing Orders"
    elif status == "completed":
        orders = Order.objects.filter(order_status='COMPLETED')
        title = "Completed Orders"
    elif status == "cancelled":
        orders = Order.objects.filter(order_status='CANCELLED')
        title = "Cancelled Orders"
    else:
        orders = Order.objects.all()
        title = "All Orders"

    return render(request, 'admin/admin_orders.html', {'orders': orders, 'title': title})
