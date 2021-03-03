from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Product, Comment, Watchlist, Bid

#index Page
def index(request):
    products= Product.objects.all()
    return render(request, "auctions/index.html",{
        "products": products
    })

#Individual Product Detail
def product_detail(request, title, id):
    #login to to use watchlist
    if not request.user.is_authenticated:
        comments = Comment.objects.all()
        products= Product.objects.filter(id=id, product_name=title)
        return render(request, "auctions/product_detail.html",{
            "products": products,
            "comments": comments
        })

    user=request.user
    watchlist = Watchlist.objects.filter(product_id=id,user=user)
    comments = Comment.objects.all()
    products= Product.objects.filter(id=id, product_name=title)
    product=[product for product in products]
    bid_amount=product[0].product_price+100
    bid = Bid.objects.filter(user=user, product_id=id)
    user_owner = False
    if(user==product[0].user):
        user_owner = True
    return render(request, "auctions/product_detail.html",{
        "products": products,
        "comments": comments,
        "watchlists": watchlist,
        "bid_amount":bid_amount,
        "bids":bid,
        "user_owner": user_owner
    })


#Login Page
def login_view(request):
    #Can't Go to register Page page without Logout
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


#Logout Page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


#Register Page
def register(request):
    #Can't Go to register Page page without Logout
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        address = request.POST["address"]
        birth_date = request.POST["birth_date"]
        first_name = username
        last_name = username

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        #Email Exists Or Not
        email_exists = User.objects.filter(email=email)
        if email_exists:
            return render(request, "auctions/register.html", {
                "email_message": "Email already taken."
            })

        phone_number_exists = User.objects.filter(phone_number=phone_number)
        if phone_number_exists:
            return render(request, "auctions/register.html", {
                "phone_number_message": "Phone Number already taken."
            })

        #Phone Number Exists Or Not

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password, 
                birth_date=birth_date,
                address= address,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name
                )
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#Profile
def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    user = User.objects.get(username=request.user)

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        address = request.POST["address"]

        user.first_name = first_name
        user.last_name = last_name
        user.address = address
            
        user.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/profile.html", {
                "existing_first_name": user.first_name,
                "existing_last_name": user.last_name,
                "existing_email": user.email,
                "existing_address": user.address,
                "existing_phone_number": user.phone_number,
                "existing_birth_date": user.birth_date
            })

#Auction
def product_add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":

        # Add Products for Auctions
        product_name = request.POST["product_name"]
        product_price = request.POST["product_price"]
        product_img = request.POST["product_img"]
        product_category = request.POST["product_category"]

        user = User.objects.get(username=request.user)

        product_add = Product(
            user = user, 
            product_name = product_name,
            product_category = product_category, 
            product_price = product_price,
            product_img = product_img
            )
        product_add.save()
        return render(request, "auctions/index.html")
    else:
        return render(request, "auctions/product_add.html")


#Category
def product_category(request):
    comments= Comment.objects.all()
    if request.method == "POST":
        category = request.POST["category"]
        product = Product.objects.filter(product_category=category)
        return render(request, "auctions/product_category.html",{
            "products":product,
            "category": category,
            "comments": comments
        })
    else:
        product = Product.objects.all()
        return render(request, "auctions/product_category.html",{
            "products" : product,
            "comments" : comments
        })

#My Products
def product_my(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    product = Product.objects.filter(user= request.user)
    return render(request, "auctions/product_my.html",{
            "products":product
        })

def product_comment(request):
    if request.method=="POST":
        user = request.user
        product_id = request.POST["product"]
        comment = request.POST["comment"]
        newcomment = Comment(user=user, product_id=product_id, comment=comment)
        newcomment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Product WatchList
def product_watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    watchlist = Watchlist.objects.filter(user= request.user)
    return render(request, "auctions/product_watchlist.html",{
            "watchlists":watchlist
        })

#Product Add to WatchList
def product_watchlist_add(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user= request.user
    products = Product.objects.filter(id=id)
    product_id = [product.id for product in products]
    watchlist = Watchlist(user=user, product_id=product_id[0])
    watchlist.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#Product Remove from Watchlist
def product_watchlist_remove(request, id):
    Watchlist.objects.get(product_id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def product_bid(request, productid, amount):
    user = request.user
    product = Product.objects.get(id=productid)
    product.product_price = amount
    product.save()
    bid_found = Bid.objects.filter(product_id=productid)
    
    #Delete old Amount and user 
    if(bid_found):
        bid_found.delete()

    bid = Bid(user=user, product=product, amount=amount)
    bid.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Product Close
def product_close(request, productid):
    product = Product.objects.filter(id=productid)
    if(product):
        prod = [prod for prod in product]
        if(request.user == prod[0].user):
            bids = Bid.objects.filter(product_id=productid)
            bid = [bid for bid in bids]
            biduser = "No"
            price = "none"
            if(bids):
                biduser=bid[0].user
                price=bid[0].product.product_price

            product.delete()
            return render(request, "auctions/product_close.html",{
                    "biduser": biduser,
                    "price":price
                })
        else:
            return render(request, "auctions/product_close.html",{
                "message" : "Not Authorize to delete"
            })
    else:
        return render(request, "auctions/product_close.html",{
                "message" : "Not Authorize to delete"
            })

