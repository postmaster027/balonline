from posts.models import Post
from cbrexchange.models import Quote
from weather.models import Forecast
from ymapscatalog.models import Traffic, Firm

from django.contrib import admin

admin.site.register(Post)
admin.site.register(Quote)
admin.site.register(Forecast)
admin.site.register(Traffic)
admin.site.register(Firm)
