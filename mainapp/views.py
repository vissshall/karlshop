from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import randint

from django.conf import settings
from django.core.mail import send_mail

from karlshop.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay
from .models import *


def homePage(Request):
    data = Product.objects.all()
    data = data[::-1]
    data = data[0:6]

    items=Maincategory.objects.all()
    item_list=[]
    for item in items.values():
        item_list.append(item)
    Request.session['maincategories']=item_list

    items=Subcategory.objects.all()
    item_list=[]
    for item in items.values():
        item_list.append(item)
    Request.session['subcategories']=item_list


    items=Brand.objects.all()
    item_list=[]
    for item in items.values():
        item_list.append(item)
    Request.session['brands']=item_list    
    
    return render(Request, "index.html", {'data': data})


def shopPage(Request, mc, sc, br):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if (mc == 'All' and sc == 'All' and br == 'All'):
        data = Product.objects.all()
    elif (mc != 'All' and sc == 'All' and br == 'All'):
        data = Product.objects.filter(
            maincategory=Maincategory.objects.get(name=mc))
    elif (mc == 'All' and sc != 'All' and br == 'All'):
        data = Product.objects.filter(
            subcategory=Subcategory.objects.get(name=sc))
    elif (mc == 'All' and sc == 'All' and br != 'All'):
        data = Product.objects.filter(brand=Brand.objects.get(name=br))
    elif (mc != 'All' and sc != 'All' and br == 'All'):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc))
    elif (mc != 'All' and sc == 'All' and br != 'All'):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), brand=Brand.objects.get(name=br))
    elif (mc == 'All' and sc != 'All' and br != 'All'):
        data = Product.objects.filter(subcategory=Subcategory.objects.get(
            name=sc), brand=Brand.objects.get(name=br))
    else:
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc), brand=Brand.objects.get(name=br))
    data = data[::-1]
    return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'mc': mc, 'sc': sc, 'br': br})


def priceFilterPage(Request):
    if (Request.method == "POST"):
        mc = Request.POST.get("mc")
        sc = Request.POST.get("sc")
        br = Request.POST.get("br")
        min = int(Request.POST.get("min"))
        max = int(Request.POST.get("max"))
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        brand = Brand.objects.all()
        if (mc == 'All' and sc == 'All' and br == 'All'):
            data = Product.objects.filter(
                finalprice__gte=min, finalprice__lte=max)
        elif (mc != 'All' and sc == 'All' and br == 'All'):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(
                name=mc), finalprice__gte=min, finalprice__lte=max)
        elif (mc == 'All' and sc != 'All' and br == 'All'):
            data = Product.objects.filter(subcategory=Subcategory.objects.get(
                name=sc), finalprice__gte=min, finalprice__lte=max)
        elif (mc == 'All' and sc == 'All' and br != 'All'):
            data = Product.objects.filter(brand=Brand.objects.get(
                name=br), finalprice__gte=min, finalprice__lte=max)
        elif (mc != 'All' and sc != 'All' and br == 'All'):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(
                name=mc), subcategory=Subcategory.objects.get(name=sc), finalprice__gte=min, finalprice__lte=max)
        elif (mc != 'All' and sc == 'All' and br != 'All'):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(
                name=mc), brand=Brand.objects.get(name=br), finalprice__gte=min, finalprice__lte=max)
        elif (mc == 'All' and sc != 'All' and br != 'All'):
            data = Product.objects.filter(subcategory=Subcategory.objects.get(
                name=sc), brand=Brand.objects.get(name=br), finalprice__gte=min, finalprice__lte=max)
        else:
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc), subcategory=Subcategory.objects.get(
                name=sc), brand=Brand.objects.get(name=br), finalprice__gte=min, finalprice__lte=max)
        data = data[::-1]
        return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'mc': mc, 'sc': sc, 'br': br})
    else:
        return HttpResponseRedirect("/shop/All/All/All")


def searchPage(Request):
    if (Request.method == "POST"):
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        brand = Brand.objects.all()
        search = Request.POST.get("search")
        data = Product.objects.filter(Q(name__icontains=search) | Q(color__icontains=search) | Q(
            size__icontains=search) | Q(stock__icontains=search) | Q(description__icontains=search))
        data = data[::-1]
        return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'mc': "All", 'sc': "All", 'br': "All"})
    else:
        return HttpResponseRedirect("/shop/All/All/All")


def singleProductPage(Request, num):
    data = Product.objects.get(id=num)
    relatedProducts = Product.objects.filter(
        brand=data.brand, maincategory=data.maincategory, subcategory=data.subcategory)
    return render(Request, "product-details.html", {'data': data, 'relatedProducts': relatedProducts})


def cartPage(Request):
    cart = Request.session.get("cart", None)
    return render(Request, "cart.html", {'cart': cart})


@login_required(login_url='/login')
def checkoutPage(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=user.username)
    return render(Request, "checkout.html", {'buyer': buyer})


client=razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login')
def placeOrderPage(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=user.username)
        cart = Request.session.get("cart", None)
        count = Request.session.get("count", 0)
        mode = Request.POST.get("mode")
        if (count == 0):
            return HttpResponseRedirect("/cart/")
        else:
            checkout = Checkout()
            checkout.buyer = buyer
            checkout.subtotal = Request.session.get("subtotal", 0)
            checkout.shipping = Request.session.get("shipping", 0)
            checkout.total = Request.session.get("total", 0)
            checkout.save()

            for item in cart.values():
                cp = CheckoutProduct()
                p = Product.objects.get(id=item['id'])
                cp.product = p
                cp.checkout = checkout
                cp.qty = item['qty']
                cp.total = item['total']
                cp.save()
            Request.session['cart'] = {}
            Request.session['count'] = 0
            Request.session['subtotal'] = 0
            Request.session['shipping'] = 0
            Request.session['total'] = 0
            if(mode=='COD'):
                return HttpResponseRedirect("/confirmation")
            else:
                orderAmount= checkout.total*100
                orderCurrency="INR"
                paymentOrder=client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
                paymentId=paymentOrder['id']
                checkout.paymentMode=1
                checkout.save()
                return render(Request,"pay.html",{
                    "amount":orderAmount,
                    "api_key":RAZORPAY_API_KEY,
                    "order_id":paymentId,
                    "User":buyer
                })
            

@login_required(login_url="/login/")
def paymentSuccess(request,rppid,rpoid,rpsid):
    buyer=Buyer.objects.get(username=request.server)
    check=Checkout.objects.filter(user=buyer)
    check=check[::-1]
    check=check[0]
    check.rppid= rppid
    check.paymentstatus=1
    check.save()
    return HttpResponseRedirect("/confirmation/")

@login_required(login_url="/login/")
def confirmationPage(Request):
    return render(Request, 'confirmation.html')


def loginPage(Request):
    if (Request.method == "POST"):
        username = Request.POST.get("username")
        password = Request.POST.get("password")
        user = authenticate(username=username, password=password)
        if (user is not None):
            login(Request, user)
            if (user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(Request, "Invalid Username or Password!!!")
    return render(Request, "login.html")


def signupPage(Request):
    if (Request.method == "POST"):
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if (password == cpassword):
            name = Request.POST.get("name")
            email = Request.POST.get("email")
            phone = Request.POST.get("phone")
            username = Request.POST.get("username")
            try:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                buyer = Buyer()
                buyer.name = name
                buyer.email = email
                buyer.phone = phone
                buyer.username = username
                buyer.save()
                return HttpResponseRedirect("/login/")
            except:
                messages.error(Request, "User name already taken!!")
        else:
            messages.error(
                Request, "Password and Confirm Password doesn't matches!!")
    return render(Request, "signup.html")


def logoutPage(Request):
    logout(Request)
    return HttpResponseRedirect("/login/")


@login_required(login_url="/login/")
def profilePage(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=user.username)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        checkout = Checkout.objects.filter(buyer=buyer)
        orders = []
        for item in checkout:
            cp = CheckoutProduct.objects.filter(checkout=item)
            orders.append({'checkout': item, 'checkoutProducts': cp})
    return render(Request, "profile.html", {'buyer': buyer, 'wishlist': wishlist, 'orders': orders})


@login_required(login_url="/login/")
def updateProfilePage(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=user.username)
        if (Request.method == "POST"):
            buyer.name = Request.POST.get("name")
            buyer.email = Request.POST.get("email")
            buyer.phone = Request.POST.get("phone")
            buyer.addressline1 = Request.POST.get("addressline1")
            buyer.addressline2 = Request.POST.get("addressline2")
            buyer.addressline3 = Request.POST.get("addressline3")
            buyer.pin = Request.POST.get("pin")
            buyer.city = Request.POST.get("city")
            buyer.state = Request.POST.get("state")
            if (Request.FILES.get("pic")):
                buyer.pic = Request.FILES.get("pic")
            buyer.save()
            return HttpResponseRedirect("/profile/")

    return render(Request, "update-profile.html", {'buyer': buyer})


def addToCartPage(Request):
    if (Request.method == "POST"):
        id = Request.POST.get("id")
        qty = int(Request.POST.get("qty"))
        p = Product.objects.get(id=id)
        cart = Request.session.get("cart", None)
        if (cart):
            if (id in cart.keys()):
                item = cart[id]
                item['qty'] = item['qty']+qty
                item['total'] = item['total']+qty*item['price']
                cart[id] = item
            else:
                cart.setdefault(id, {'id': id, 'name': p.name, 'color': p.color, 'size': p.size,
                                'price': p.finalprice, 'qty': qty, 'total': p.finalprice*qty, 'pic': p.pic1.url})
        else:
            cart = {id: {'id': id, 'name': p.name, 'color': p.color, 'size': p.size,
                         'price': p.finalprice, 'qty': qty, 'total': p.finalprice*qty, 'pic': p.pic1.url}}
        Request.session['cart'] = cart
        subtotal = 0
        shipping = 0
        count = 0
        for item in cart.values():
            subtotal = subtotal+item['total']
            count = count+item['qty']
        if (subtotal > 0 and subtotal < 1000):
            shipping = 150
        total = subtotal+shipping
        Request.session['subtotal'] = subtotal
        Request.session['shipping'] = shipping
        Request.session['total'] = total
        Request.session['count'] = count
        Request.session.set_expiry(60*60*24*30)
        return HttpResponseRedirect("/cart/")
    else:
        return HttpResponseRedirect("/shop/All/All/All")


def deleteFromCartPage(Request, num):
    cart = Request.session.get("cart", None)
    if (cart):
        del cart[num]
        Request.session['cart'] = cart
        subtotal = 0
        shipping = 0
        count = 0
        for item in cart.values():
            subtotal = subtotal+item['total']
            count = count+item['qty']
        if (subtotal > 0 and subtotal < 1000):
            shipping = 150
        total = subtotal+shipping
        Request.session['subtotal'] = subtotal
        Request.session['shipping'] = shipping
        Request.session['total'] = total
        Request.session['count'] = count
        Request.session.set_expiry(60*60*24*30)
    return HttpResponseRedirect("/cart/")


def updateCartPage(Request, num, op):
    cart = Request.session.get("cart", None)
    if (cart):
        item = cart[num]
        if (op == "dec" and item['qty'] == 1):
            return HttpResponseRedirect("/cart/")
        elif (op == "dec"):
            item['qty'] = item['qty']-1
            item['total'] = item['total']-item['price']
        else:
            item['qty'] = item['qty']+1
            item['total'] = item['total']+item['price']
        cart[num] = item
        Request.session['cart'] = cart
        subtotal = 0
        shipping = 0
        count = 0
        for item in cart.values():
            subtotal = subtotal+item['total']
            count = count+item['qty']
        if (subtotal > 0 and subtotal < 1000):
            shipping = 150
        total = subtotal+shipping
        Request.session['subtotal'] = subtotal
        Request.session['shipping'] = shipping
        Request.session['total'] = total
        Request.session['count'] = count
        Request.session.set_expiry(60*60*24*30)
    return HttpResponseRedirect("/cart/")


@login_required(login_url="/login/")
def addToWishlistPage(Request, num):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=user.username)
        p = Product.objects.get(id=num)
        try:
            wish = Wishlist.objects.get(buyer=buyer, product=p)
        except:
            wishlist = Wishlist()
            wishlist.buyer = buyer
            wishlist.product = p
            wishlist.save()
        return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def removeFromWishlistPage(Request, num):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=user.username)
        wishlist = Wishlist.objects.get(id=num)
        if (wishlist and wishlist.buyer == buyer):
            wishlist.delete()
        return HttpResponseRedirect("/profile/")


def contactUsPage(Request):
    if (Request.method == "POST"):
        c = Contact()
        c.name = Request.POST.get("name")
        c.email = Request.POST.get("email")
        c.phone = Request.POST.get("phone")
        c.subject = Request.POST.get("subject")
        c.message = Request.POST.get("message")
        c.save()
        messages.success(
            Request, "Thanks to share your Query! Our team will contact You soon.")
    return render(Request, 'contact.html')


def forgetPasswordPage1(Request):
    if (Request.method == "POST"):
        try:
            user = Buyer.objects.get(username=Request.POST.get("username"))
            num = randint(100000, 999999)
            user.otp = num
            user.save()
            subject = 'OTP for Password Reset : Team KarlShop'
            message = """
                        Hello User!!
                        Your OTP for password reset is """+str(num)+"""
                        Do not share OTP with anyone
                        Team : KarlShop
                        """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)

            Request.session['reset-password-username']=user.username
            return HttpResponseRedirect("/gorget-password2/")
        except:
            messages.error(Request, "Username Not Found!!!")
    return render(Request,"forget-password1.html")


def forgetPasswordPage2(Request):
    if(Request.method=="POST"):
        username=Request.session.get("reset-password-username")
        if(username):
            try:
                user= Buyer.objects.get(username=username)
                otp=int(Request.POST.get("otp"))
                if(user.otp==otp):
                  return HttpResponseRedirect("/forget-password3/")
                else:
                    messages.error(Request,"Invalid otp!!")  
            except:
                messages.error(Request,"UnAuthorised!!")
        else:
            messages.error(Request,"UnAuthorised!!")
    return render(Request,"forget-password2.html")


def forgetPasswordPage3(Request):
    if(Request.method=="POST"):
        username=Request.session.get("reset-password-username")
        if(username):
            try:
                buyer= Buyer.objects.get(username=username)
                password=Request.POST.get("password")
                cpassword=Request.POST.get("cpassword")
                if(password==cpassword):
                    user=User.objects.get(username=buyer.username)
                    user.set_password(password)
                    user.save()
                    del Request.session['reset-password-username']
                    return HttpResponseRedirect("/login/")
                else:
                    messages.error(Request,"password and confirm password doesnt matches!")
            except:
                messages.error(Request,"UnAuthorised!!")
        else:
            messages.error(Request,"UnAuthorised!!")
    return render(Request,"forget-password3.html")
