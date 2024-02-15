from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import User, Category,listing, comment, commentForm, Bid


def index(request):
   
   pass

def bidlisting(request, id):
    bidlisting_data= listing.objects.get(pk=id) #Retrieve the listing object with the given id from  database
    listinginwatchlist= request.user in bidlisting_data.watchlist.all() # check if current user in watchlist and determine what to display either add to watchlit or remove.....
    allcomment=comment.objects.filter(listings=bidlisting_data) #retrieve all comments that in this particular listing
    ownership= request.user.username == bidlisting_data.lister.username #Check if the current user is the owner
    return render(request,'auctions/bidlisting.html',{
        'listing': bidlisting_data,
        'listinginwatchlist':listinginwatchlist,
        'ownership': ownership,
        'allcomment': allcomment,
    })

def addtowatchlist(request,id):
    listdata= listing.objects.get(pk=id) #Retrieve the listing object with the given id from  database
    usercurrently= request.user # get current user
    listdata.watchlist.add(usercurrently) #add listing to current user watchlist
    return HttpResponseRedirect(reverse('bidlisting',args=(id, )))

def removefromwatchlist(request, id):
    listdata= listing.objects.get(pk=id) #Retrieve the listing object with the given id from  database
    usercurrently= request.user # get current user
    listdata.watchlist.remove(usercurrently) # remove listing from current user watchlist
    return HttpResponseRedirect(reverse('bidlisting',args=(id, )))

def watchlistview(request):
    usercurently= request.user # get current user
    alllisting= usercurently.watchlists.all() # retrieve all listing that in current user watchlist
    return render(request, "auctions/watchlist.html",{
        "listings":alllisting,
    })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("active_listings"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("active_listings"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("active_listings"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method =="POST": 
        #extract data from post request
        title= request.POST["title"]
        story= request.POST["story"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category= request.POST["category"]

        category_info = Category.objects.get(Category=category) #Get the categorys from the model
        User= request.user #Get cuurent user
        bid= Bid(bid=float(price), user=User) #create a new bid object with price and user

        bid.save() # save 

        # Create a new listing with the provided data.
        
        createListing= listing(
            title= title,
            story=story,
            imageURL=imageurl,
            price=bid,
            category= category_info,
            lister=User
        )
        createListing.save() #save the listing

        return HttpResponseRedirect(reverse(active_listings))


        

    else:
        categories = Category.objects.all() #show all category in the class
        return render(request, "auctions/newlisting.html",{
            'category': categories})
            



def active_listings(request):
    active_listings = listing.objects.filter(activity=True) #this is for getting all active listing
    categories = Category.objects.all() # for getting all category
    return render(request, "auctions/active_listing.html", {
        "active_listings": active_listings,
        'category': categories,
        })


def listingcategories(request):
    if request.method == 'POST':
        form_category = request.POST["category"] # get the selected category from the post request
        category = Category.objects.get(Category= form_category) #get the corresponding category from the database
        active_listings = listing.objects.filter(activity=True, category=category) #this is for getting all active listing
        categories = Category.objects.all() # for getting all category
        return render(request, "auctions/active_listing.html", {
            "active_listings": active_listings,
            'category': categories
        })
    


def addbid(request, id):
    newbid = request.POST["newbid"] # get the new bid amount from post request
    listing_detail=listing.objects.get(pk=id) # get the listing details that correspond that id
    allcomment=comment.objects.filter(listings=listing_detail) # get all comments that correspond to that listing
    listinginwatchlist= request.user in listing_detail.watchlist.all() #check if current user in watchlist to make decision what to display either add to.. or remove from..
    ownership= request.user.username == listing_detail.lister.username #check if the cuurent user is the owner of the listing
    if int(newbid) > listing_detail.price.bid:
        #Create a new Bid object with the specified bid amount and user.
        updatebid= Bid(user=request.user, bid=int(newbid))
        updatebid.save()
        #update listing price to the new bid amount
        listing_detail.price = updatebid
        listing_detail.save()
        return render(request, "auctions/bidlisting.html",{
            "listing": listing_detail,
            "message":" Successfull Bid",
            "updated": True,
            'allcomment': allcomment,
            'listinginwatchlist':listinginwatchlist,
            'ownership': ownership,

        })
    else:
        return render(request, "auctions/bidlisting.html",{
            "listing": listing_detail,
            "message":"Please Enter a Higher Bid",
            "updated": False,
            'allcomment': allcomment,
            'listinginwatchlist':listinginwatchlist,
            'ownership': ownership,
            

        })



def closeauctions(request, id):
    listing_detail=listing.objects.get(pk=id)# get the listing details that correspond that id
    allcomment=comment.objects.filter(listings=listing_detail) # get all comments that correspond to that listing
    ownership= request.user.username == listing_detail.lister.username #check if the cuurent user is the owner of the listing
    listinginwatchlist= request.user in listing_detail.watchlist.all()#check if current user in watchlist to make decision what to display either add to.. or remove from..
    listing_detail.activity = False # Set the listing's activity status to False, indicating that the auction is closed.
    listing_detail.save()
    return render(request, "auctions/bidlisting.html",{
            "listing": listing_detail,
            "message":"Auction Closed Succefully",
            "updated": True,
            'ownership': ownership,
            'listinginwatchlist':listinginwatchlist,
            'allcomment': allcomment,

        })






def addcomment(request, id):
    listing_detail = get_object_or_404(listing, pk=id)#get the listing details that correspond that id or return 404 error if not found

    if request.method == 'POST':
        form = commentForm(request.POST) # Create  form object with  post data.
        if form.is_valid():
            message = form.cleaned_data['newcomment']# Extract the cleaned comment message from the form data.
            if message.strip():  # Check if the comment is not empty or only contains spaces
                new_comment = comment(  # Create a new comment object
                    author=request.user,
                    listings=listing_detail,
                    message=message
                )
                new_comment.save()
                messages.success(request, 'Comment added successfully.')
            
        
    return HttpResponseRedirect(reverse('bidlisting', args=(id,)))
