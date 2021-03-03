from django.contrib import admin
from .models import User, Product, Comment, Watchlist, Bid

# Register your models here

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)




