from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm ,Customer ,CustomerProfileForm 
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

 
class ProductView(View):
    def get(self ,request):
        totalitem =0
        topwears = Product.objects.filter(category='TW')  
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        randoms = Product.objects.filter(category='R')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html' ,{ 'laptops':laptops, 'randoms':randoms, 'topwears':topwears ,'bottomwears':bottomwears , 'mobiles':mobiles , 'totalitem':totalitem})



 
class ProductDetailView(View):
    def get(self,request, pk):
        totalitem =0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False  
        if request.user.is_authenticated:
            if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html', {'product':product , 'item_already_in_cart':item_already_in_cart ,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user ,product=product).save()
    return redirect('/cart/')

@login_required
def buy_now(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user ,product=product).save()
    return redirect('/cart/')
    # return render(request, 'app/addtocart.html')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem = 0
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity* p.product.discount_prize)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html' ,{'carts':cart ,'totalamount':totalamount ,'amount':amount ,'totalitem':totalitem})
        else:
          return render(request ,'app/emptycart.html')

def pluse_cart(request):
 if request.method == 'GET':
    prod_id =request.GET['prod_id']
    c =Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount = (p.quantity* p.product.discount_prize)
        amount += tempamount
 
    data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount':amount + shipping_amount
        }
    return JsonResponse(data)

def minus_cart(request):
 if request.method == 'GET':
    prod_id =request.GET['prod_id']
    c =Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount = (p.quantity* p.product.discount_prize)
        amount += tempamount
 
    data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount':amount + shipping_amount
        }
    return JsonResponse(data)

# // remove cart  is not working ! see video 5.00 -5.40 ===https://www.youtube.com/watch?v=I6rR3Se72BU

def remove_cart(request):
 if request.method == 'GET':
    prod_id =request.GET['prod_id']
    c =Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount = (p.quantity * p.product.discount_prize)
        amount += tempamount
 
    data = {
            'amount' : amount,
            'totalamount':amount + shipping_amount
        }
    return JsonResponse(data)

@login_required
def buy_now(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/buynow.html',{'totalitem':totalitem})
 
@method_decorator(login_required ,name="dispatch")
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user)) 
        form = CustomerProfileForm()
        add = Customer.objects.filter(user=request.user)

        if add == 0:
            return redirect("/profile/")
        return render(request ,'app/profile.html' ,{'form':form ,'active':'btn-primary' ,'totalitem':totalitem})
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name =form.cleaned_data['name']
            locality =form.cleaned_data['locality']
            city =form.cleaned_data['city']
            zipcode =form.cleaned_data['zipcode']
            state =form.cleaned_data['state']
            reg = Customer(user=user ,name=name,locality=locality,city=city,zipcode=zipcode ,state=state)
            reg.save()
            messages.success(request,'Congratulations !! Profile Update Successfully | ')
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

         

        

@login_required
def address(request):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    print(add)
    if add == 0:
       return redirect('/cart/')
    return render(request, 'app/address.html' , {'add':add ,'active':'btn-primary' ,'totalitem':totalitem})

 
# class MobileDetailview(View):
#  def get(self , request ,pk):
def  mobile(request):
    # product = Product.objects.get(pk=pk)
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        mobiles = Product.objects.filter(category='M')
    return render(request, 'app/mobile.html',{'mobiles':mobiles ,'totalitem':totalitem})
    # return render(request, 'app/mobile.html',{'mobiles':mobiles ,'totalitem':totalitem ,'product':product})


def laptop(request):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    laptops = Product.objects.filter(category='L')
    return render(request, 'app/laptop.html',{'laptops':laptops ,'totalitem':totalitem})

def topwear(request):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    topwears = Product.objects.filter(category='TW')
    return render(request, 'app/topwears.html',{'topwears':topwears ,'totalitem':totalitem})

def bottomwear(request):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    bottomwears = Product.objects.filter(category='BW')
    return render(request, 'app/bottomwears.html',{'bottomwears':bottomwears ,'totalitem':totalitem})


 
class CustomerRegistrationView(View):
    def get(self ,request):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form ,'totalitem':totalitem})

    def post(self ,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request , 'Congratulations!! Registered Successfully!✔ Please login ^_^')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    print(cart_items)
    amount =0.0
    shipping_amount = 70.0
    totalamount =0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_prize)
            amount += tempamount
            totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add , 'totalamount':totalamount ,'cart_items':cart_items ,'totalitem':totalitem})

@login_required
def payment_done(request):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    custid =request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user , customer=customer , product=c.product ,quantity=c.quantity ).save()
        c.delete()
    messages.success(request , 'Thank You !! For Buying Our Product !! ^_^ !!  ')
         
    return redirect("/orders/")

@login_required
def payment_done2(request):
     
        # messages.success(request , 'Thank You !! For Buying Our Product !! ^_^ !!  ')
         
    return render(request, 'app/paymentdone.html')




@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op ,'totalitem':totalitem})