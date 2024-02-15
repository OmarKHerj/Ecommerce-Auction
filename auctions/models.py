from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms





class User(AbstractUser):
    pass



class Category(models.Model):
    Category=models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.Category


class Bid(models.Model):
    bid= models.FloatField(default=0)
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True, related_name='userbid')
    
   

class listing(models.Model):
    title= models.CharField(max_length=40)
    story= models.TextField(null=True)
    price=models.ForeignKey(Bid,on_delete=models.CASCADE,blank=True,null=True,  related_name='bidprice')                        
    imageURL= models.CharField(max_length=1000,blank=True,null=True)
    
    
    activity=models.BooleanField(default=True)
    
    lister=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True, related_name='user')
    category=models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True,  related_name='category')
    date_added = models.DateTimeField(auto_now_add=True)
    watchlist=models.ManyToManyField(User, blank=True,null=True, related_name="watchlists")

    def __str__(self):
        return self.title
    



class comment(models.Model):
    message=models.TextField(blank= True, null= True)
    author= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True, related_name='usercomments')
    timestamp= models.DateTimeField(auto_now_add=True)
    listings=models.ForeignKey(listing, on_delete=models.CASCADE, blank=True, null= True, related_name='listingcomments')


    def __str__(self):
        return f"{self.author} Comment on {self.listings}"


class commentForm(forms.Form):
    newcomment = forms.CharField(widget=forms.Textarea)