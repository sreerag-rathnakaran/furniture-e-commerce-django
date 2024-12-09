from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import razorpay
from django.conf import settings

from django.db.models import Q





def index(req):
    data=Product.objects.all()
    return render(req,'index.html',{'data':data})


@login_required(login_url='register_customer')
def shop(request):
    data=Product.objects.all()
    return render(request,'shop.html',{'data':data})

def blog(request):
    review = Review.objects.all().order_by('-id') [0:3]
    return render(request, 'blog.html', {'review':review})

def admin(request):
    return render(request,'admin.html')

def display_customer(req):
    data=Customer.objects.all()
    return render(req,'display_customer.html',{'data':data})


    


def sellers(request):
    return render(request,'sellers.html')







# category CRUD

def addcategory(request):
    return render(request,'addcategory.html')

def add_category(req):
    if req.method=='POST':
        cn=req.POST['cname']
        cd=req.POST['cdescrp']
        cim=req.FILES['cimg']
        C=Category.objects.create(name=cn,description=cd,image=cim)
        C.save()
        return HttpResponse('SUCCESS')
    
def display_category(req):
    data=Category.objects.all()
    return render(req,'display_category.html',{'data':data})


    
def update_category(req,id):
    data=Category.objects.get(id=id)    
    return render(req,'update_category.html',{'data':data})

def update_categorydetails(req,id):

    if req.method=='POST':
        cn=req.POST['cname']
        cd=req.POST['cdescrp']

        try:
            cim=req.FILES['cimg']
            
            fs=FileSystemStorage()
            file=fs.save(cim.name,cim)

        except MultiValueDictKeyError:
            file=Category.objects.get(id=id).image
        Category.objects.filter(id=id).update(name=cn,description=cd,image=file)

        return redirect (display_category)

def delete_category(req,id):
    cdata=Category.objects.get(id=id)
    cdata.delete()
    return redirect(display_category)




# product CRUD

def addproduct(request):
    data=Category.objects.all()
    return render(request,'addproduct.html',{'data':data})

def add_product(req):

    if req.method=='POST':
        pc=req.POST['pcat']
        pn=req.POST['pname']
        pd=req.POST['pdescrp']
        ppr=req.POST['pprice']
        pop=req.POST.get('poprice')
        pst=req.POST['pstock']
        pim=req.FILES['pimg']

        if pop:
            C=Category.objects.get(id=pc) 
            S=Sellerdetails.objects.get(id=req.user.seller.id)
            P=Product.objects.create(seller=S,category=C,name=pn,description=pd,price=ppr,sale_price=pop,is_sale=True,stock=pst,image=pim)
            P.save()
            return HttpResponse('SUCCESS')

        C=Category.objects.get(id=pc)
        S=Sellerdetails.objects.get(id=req.user.seller.id)
        P=Product.objects.create(seller=S,category=C,name=pn,description=pd,price=ppr,is_sale=False,stock=pst,image=pim)
        P.save()
        return HttpResponse('SUCCESS')
    

def display_product(req):
    data=Product.objects.all()
    return render(req,'display_product.html',{'data':data})

def update_product(req,id):
    data=Product.objects.get(id=id)    
    return render(req,'update_product.html',{'data':data})


def update_productdetails(req,id):
    if req.method=='POST':
        # pc=req.POST['pcat']
        pn=req.POST['pname']
        pd=req.POST['pdescrp']
        ppr=req.POST['pprice']
        pop=req.POST.get('poprice')
        # pis=req.POST['pissale']
        pst=req.POST['pstock']
        try:
            pim=req.FILES['pimg']
            
            fs=FileSystemStorage()
            file=fs.save(pim.name,pim)

        except MultiValueDictKeyError:
            file=Product.objects.get(id=id).image
        Product.objects.filter(id=id).update(name=pn,description=pd,price=ppr,sale_price=pop,stock=pst,image=file)
        return redirect(display_product)

    else:
        return HttpResponse('error')

def delete_product(req,id):
    pdata=Product.objects.get(id=id)
    pdata.delete()
    return redirect(display_category)





# customer registration

def register_customer(req):
    if req.method=='POST':
        un=req.POST['uname']
        fn=req.POST['fname']
        ag=req.POST['age']
        mob=req.POST['mob']
        em=req.POST['email']
        pd=req.POST['password']
        im=req.FILES['image']

        Cus=CustomUser.objects.create_user(username=un,password=pd,email=em,is_customer=True)
        c=Customer.objects.create(Name=fn,Age=ag,Phone=mob,Email=em,user=Cus,Image=im)
        c.save()
        user = authenticate(username=un, password=pd)
        if user is not None:
            login(req, user)
            messages.success(req, 'Registered Successfully')
            return redirect(index)
        return HttpResponse('saved..')
    else:
        return render (req, 'register_customer.html')
    

# Customer details update

def update_customer(req,id):
    data=Customer.objects.get(id=id)
    return render(req,'update_customer.html',{'data':data})

def update_customerdetails(req,id):

    if req.method=='POST':
        un=req.POST['uname']
        fn=req.POST['fname']
        ag=req.POST['age']
        mob=req.POST['mob']
        em=req.POST['email']
        pd=req.POST['password']
        

        try:
            im=req.FILES['image']
            
            fs=FileSystemStorage()
            file=fs.save(im.name,im)

        except MultiValueDictKeyError:
            file=Customer.objects.get(id=id).Image

        customer = Customer.objects.get(id=id)
        customer.user.username = un
        customer.Name = fn
        customer.Email = em
        customer.Phone=mob
        customer.user.email = em
        customer.user.set_password(pd)
        customer.user.save()
        customer.Image = file
        customer.save()
        messages.success(req, 'Updated Successfully')
        return redirect (userprofile)
        
    
# customer login

def LoginCustomer(req):
    if req.method=='POST':
        un=req.POST['username']
        pd=req.POST['password']
        user=authenticate(req,username=un,password=pd)

        if user is not None:
            
            if user.is_customer==True:
                login(req,user)
                messages.success(req, 'Logined Successfully')
                return redirect(index)
        else:
            messages.error(req, 'Invalid Credentials')  
            return redirect(register_customer)  
    else:
        redirect(register_customer)


@login_required(login_url='register_customer')
def LogoutCustomer(req):
    logout(req)
    messages.success(req, 'Logged out Successfully')
    return redirect(index)


@login_required(login_url='register_customer')
def userprofile(req,):
    data=Customer.objects.get(user=req.user)
    return render(req,'userprofile.html',{'data':data})








# seller registration

def register_seller(req):
    if req.method=='POST':
        un=req.POST['uname']
        sn=req.POST['fname']
        sd=req.POST['sdescrp']
        sm=req.POST['semail']
        spd=req.POST['password']
        sdt=req.POST['sdt']
        sim=req.FILES['simg']

        Seller=CustomUser.objects.create_user(username=un,password=spd,email=sm,)
        s=Sellerdetails.objects.create(username=un,name=sn,email=sm,Logo=sim,description=sd,application_date=sdt,user=Seller)
        s.save()
        return HttpResponse('saved..')
    else:
        return render (req,'register_seller.html')
    
# List of pending sellers

def approve_or_cancel_seller(req):
    data= Sellerdetails.objects.filter(status='Pending')
    return render(req, 'approve_or_cancel_seller.html', {'data': data})

def approve_seller(request, id):
    s= Sellerdetails.objects.get(id=id)
    s.status = 'Approved'
    s.user.is_seller=True
    s.save()
    s.user.save()
    return redirect(approve_or_cancel_seller)

def approved_seller(request):
    data= Sellerdetails.objects.filter(status='Approved')
    return render(request, 'approved_seller.html', {'data': data})

def reject_seller(request,id):
    s= Sellerdetails.objects.get(id=id)
    s.status = 'Rejected'
    s.save()
    s.user.delete()
    return redirect(approve_or_cancel_seller)


def display_seller(req):
    data=Sellerdetails.objects.get(user=req.user)
    return render(req,'display_seller.html',{'data':data})



def display_products_basedonseller(req,id):
    data=Product.objects.filter(seller__id=id)
    return render(req,'display_products_basedonseller.html',{'data':data})





    

# update sellerdetails


def update_seller(req,id):
    data=Sellerdetails.objects.get(id=id)  
    return render(req,'update_seller.html',{'data':data})


def update_sellerdetails(req,id):

    if req.method=='POST':
        un=req.POST['uname']
        sd=req.POST['sdescrp']
        sm=req.POST['semail']
        spd=req.POST['password']
        
        try:
            sim=req.FILES['simg']
            
            fs=FileSystemStorage()
            file=fs.save(sim.name,sim)

        except MultiValueDictKeyError:
            file=Sellerdetails.objects.get(id=id).Logo

        seller = Sellerdetails.objects.get(id=id)
        seller.description = sd
        seller.email = sm 
        seller.name = un 
        seller.user.username = un
        seller.user.email = sm
        seller.user.set_password(spd)
        seller.user.save()
        seller.Logo = file
        seller.save()
        return redirect (sellers)
    

# admin or seller login

def Login_admin_or_seller(req):
    if req.method=='POST':
        un=req.POST['username']
        pd=req.POST['password']
        user=authenticate(req,username=un,password=pd)

        if user is not None:
            if user.is_seller==True:
                # if user.seller.status=='Approved':
                    login(req,user)
                    return redirect(sellers)
                # else:
                #     return HttpResponse('not approved')
            
            elif user.is_superuser:
                login(req,user)
                return redirect(admin)
            
        return redirect(Login_admin_or_seller)
    else:
        return redirect(register_seller)


@login_required(login_url='register_seller')
def Logout(req):
    logout(req)
    return redirect(register_seller)



def display_sellerforadmin(req):
    data=Sellerdetails.objects.all()
    return render(req,'admin.html',{'data':data})



def single_productpage(req,id):
    data = Product.objects.get(id=id)
    cmnt = Review.objects.filter(product=data).order_by('-id') [0:3]
    return render(req,'single_productpage.html',{'data':data, 'cmnt':cmnt})

@login_required(login_url='register_customer')
def explore(req):
    data=Product.objects.all()
    return render(req,'explore.html' ,{'data':data})



@login_required(login_url='register_customer')
def cart(req):
    data=Cart.objects.filter(user=req.user)
    total = 0
    shipping = 50
    Total = 0
    for i in data:
        total += i.totalprice

    Total = total+shipping

    return render(req,'cart.html',{'data':data, 'total':total,'Total':Total})


def add_to_cart(req,id):
    p = Product.objects.get(id=id)
    quantity = 1
    totalPrice = p.price * quantity
    if Cart.objects.filter(user=req.user, product=p).exists():
        messages.success(req, 'Alredy added')
        return redirect(cart)
    
    c = Cart.objects.create(user=req.user, product=p, quantity=1, totalprice=totalPrice)
    c.save()
    messages.success(req, 'Added to cart')

    return redirect(cart)


def remove_from_cart(req,id):
    c=Cart.objects.get(id=id)
    c.delete()
    messages.error(req, 'Removed from cart')
    return redirect(cart)







def increasequantity(req,id):

    cart_item = Cart.objects.get(id=id)
    cart_item.quantity += 1

    if cart_item.product.is_sale==True:
        cart_item.totalprice = (cart_item.quantity) * cart_item.product.sale_price or cart_item.product.sale_price
        cart_item.save()

    cart_item.totalprice = (cart_item.quantity) * cart_item.product.price or cart_item.product.price
    cart_item.save()


    return redirect(cart)


def decreasequantity(req,id):

    cart_item = Cart.objects.get(id=id)

    if cart_item.quantity > 1:

        cart_item.quantity = int(cart_item.quantity - 1)

        if cart_item.product.is_sale==True:

            cart_item.totalprice = (cart_item.quantity - 1) * cart_item.product.sale_price or cart_item.product.sale_price
            cart_item.save()

        cart_item.totalprice = (cart_item.quantity - 1) * cart_item.product.price or cart_item.product.price
        cart_item.save()

    return redirect(cart)




def Proceed_to_checkout_from_cart(req):
    carts = Cart.objects.filter(user=req.user)    
    total = 0
    shipping = 50
    Total = 0
    for i in carts:
        total += i.totalprice

    Total = total+shipping

    return render(req,'checkout.html',{'data':carts, 'total':total,'Total':Total})



def Proceed_to_payment(req):
    if req.method=='POST':
        sa=req.POST['saddr']
        po=req.POST['posto']
        pin=req.POST['pin']
        di=req.POST['distr']

        cart = Cart.objects.filter(user=req.user)

        Total = 0
        shipping = 50
        for i in cart:
            Total += i.totalprice

        Total += shipping
        

        

        obj=Order.objects.create(user=req.user ,shipping_address=sa,post=po,pincode=pin,district=di,grand_total=Total)
        obj.save()

        req.session['order'] = obj.id

        for i in cart:
            
            
            orderitem = OrderItem.objects.create(order=obj,product=i.product,quantity=i.quantity,totalprice=i.totalprice)
            orderitem.save()
        
        return redirect(Payment)    
    










    

    

def Payment(req):
    id = req.session.get('order')
    order = Order.objects.get(id=id) 
    return render(req,'Payment.html',{'order':order})





razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


def onlinepayment(request,id):
     order=Order.objects.get(id=id)
     amount=int(order.grand_total * 100)
     order_data = {
         "amount" :amount ,
         'currency' :'INR',
         'receipt' : str(order.id)

     } 

     razorpay_order = razorpay_client.order.create(order_data)
     return JsonResponse({'success':True,'order_id':razorpay_order['id'],'amount':amount,'key':settings.RAZORPAY_KEY_ID})


@csrf_exempt
def verify_razor_payment(request):
    data=json.loads(request.body)
    order_id=data.get('order_id')
    razorpay_payment_id=data.get('razorpay_payment_id')
    razorpay_order_id=data.get('razorpay_order_id')
    razorpay_signature=data.get('razorpay_signature')
    
    params = {
        'razorpay_order_id':razorpay_order_id,
        'razorpay_payment_id' :razorpay_payment_id,
        'razorpay_signature' :razorpay_signature

    }


    try:
        result=razorpay_client.utility.verify_payment_signature(params)
        if result:
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.status='Orderplaced'
            order.save()
            return JsonResponse({'success':True, 'message':'Payment Successfull'})
        else:
            return JsonResponse({'success':False, 'message':'Payment Failed'})
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'success':False})
    



@login_required(login_url='register_customer')
def order(req):
    data=Order.objects.filter(user=req.user)
    return render(req,'order.html',{'data':data})


def search(req):
    q=req.GET.get('q')
    data=Product.objects.filter(Q(name__icontains=q))
    return render(req,'search.html',{'data':data})


def offerproducts(req):
    data=Product.objects.all()
    return render(req,'offerproducts.html' ,{'data':data})



def Proceed_to_checkout(req,id):
    data= Product.objects.get(id=id)    
    total = 0
    shipping = 50
    Total = 0

    total += data.price

    Total = total+shipping

    return render(req,'checkout2.html',{'data':data, 'total':total,'Total':Total})




def Payment2(req):
    id = req.session.get('order')
    order = Order.objects.get(id=id) 
    return render(req,'payment2.html',{'order':order})





def Proceed_to_payment2(req,id):
    if req.method=='POST':
        sa=req.POST['saddr']
        po=req.POST['posto']
        pin=req.POST['pin']
        di=req.POST['distr']

        data = Product.objects.get(id=id)

        Total = 0
        shipping = 50
   
        Total += data.price

        Total += shipping
        

        

        obj=Order.objects.create(user=req.user ,shipping_address=sa,post=po,pincode=pin,district=di,grand_total=Total)
        obj.save()

        req.session['order'] = obj.id

            
            
        orderitem = OrderItem.objects.create(order=obj,product=data,totalprice=data.price,quantity=1)
        orderitem.save()
        

        return redirect(Payment2)  






def cod(req,id):
    data = Order.objects.get(id=id)
    data.is_cod = True
    data.status = 'Orderplaced'
    data.save()
    messages.success(req, 'Order placed Successfully')
    return redirect(order)

def p_b_on_category(req,category):
    cat = Category.objects.get(name=category)
    data=Product.objects.filter(category=cat)
    return render(req,'p_b_on_category.html',{'data':data})



def add_review(req):
    status = ['','Poor','Below Average','Average','Verygood','Excellent']
    if req.method=='POST':
        cont=req.POST['content']
        rating = req.POST['rating']
        product = req.POST['product']
        rstatus = status[int(rating)]
        productItem = Product.objects.get(id=product)
        R=Review.objects.create(user=req.user.customer,review=cont,rating=rating,product=productItem,status=rstatus)
        R.save()
        messages.success(req, 'succefully added')
        return redirect(req.META.get('HTTP_REFERER'))
    

def cancel_order(req,id):
    cancel=Order.objects.get(id=id)
    cancel.is_cancelled = True
    cancel.save()
    return redirect(order)

def display_orders(req):
    data=Order.objects.all()
    return render(req,'display_orders.html',{'data':data})






def orderstatus(req):
    data= Order.objects.filter(status='Orderplaced')
    return render(req, 'display_orders.html', {'data': data})





def shipped_orders(request):
    data= Order.objects.filter(status='Shipped')
    return render(request, 'shipped.html', {'data': data})


def delivered_orders(request):
    data= Order.objects.filter(status='Delivered')
    return render(request, 'delivered.html', {'data': data})


def shipped(request, id):
    s= Order.objects.get(id=id)
    s.status = 'Shipped'
    s.is_shipped=True
    s.save()
    return redirect(shipped_orders)


def delivered(request, id):
    s= Order.objects.get(id=id)
    s.status = 'Delivered'
    s.is_delivered=True
    s.save()
    return redirect(delivered_orders)













    



    
    


























    
    













    


    

# def cart_detail(request):
#     customer = request.user.customer
#     cart = Cart.objects.get(customer=customer)
#     cart_items = Cart.objects.filter(cart=cart)
#     return render(request, 'cart.html', {'cart_items': cart_items, 'cart': cart})

# def remove_from_cart(request,id):
#     customer = request.user.customer
#     cart = Cart.objects.get(customer=customer)
#     cart_item = Product.objects.get(Cart, cart=cart,id=request.customer.id)
#     cart_item.delete()
#     return redirect('cart_detail')





# from django.shortcuts import render, get_object_or_404

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'store/product_list.html', {'products': products})

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'store/product_detail.html', {'product': product})

# def category_list(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     products = Product.objects.filter(category=category)
#     return render(request, 'store/category_list.html', {'category': category, 'products': products})

# from django.shortcuts import redirect
# from .models import Cart, CartItem, Product

# def add_to_cart(request, product_id):
#     customer = request.user.customer
#     product = get_object_or_404(Product, id=product_id)
#     cart, created = Cart.objects.get_or_create(customer=customer)

#     # Check if the product is already in the cart
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1  # Update quantity if already in the cart
#     cart_item.save()

#     return redirect('cart_detail')


# def cart_detail(request):
#     customer = request.user.customer
#     cart = Cart.objects.get(customer=customer)
#     cart_items = CartItem.objects.filter(cart=cart)
#     return render(request, 'store/cart_detail.html', {'cart_items': cart_items, 'cart': cart})

# def remove_from_cart(request, product_id):
#     customer = request.user.customer
#     cart = Cart.objects.get(customer=customer)
#     cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
#     cart_item.delete()
#     return redirect('cart_detail')

# from django.utils import timezone
# from .models import Order, OrderItem

# def create_order(request):
#     customer = request.user.customer
#     cart = Cart.objects.get(customer=customer)
#     cart_items = CartItem.objects.filter(cart=cart)

#     # Create the order
#     order = Order.objects.create(customer=customer, ordered_at=timezone.now())
    
#     # Create order items
#     for item in cart_items:
#         OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
    
#     # Clear the cart after creating the order
#     cart_items.delete()
    
#     return redirect('order_detail', order_id=order.id)

# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     order_items = OrderItem.objects.filter(order=order)
#     return render(request, 'store/order_detail.html', {'order': order, 'order_items': order_items})
