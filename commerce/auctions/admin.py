from typing import List
from django.contrib import admin
from .models import Bids, Comments, Listings, User, Watchlists

# Register your models here.

admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Watchlists)