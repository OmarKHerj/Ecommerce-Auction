from django.contrib import admin
from .models import listing,Category, User, comment, Bid

# Register your models here.
admin.site.register(listing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(comment)
admin.site.register(Bid)
