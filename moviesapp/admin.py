from django.contrib import admin
from moviesapp.models import User, Collection, Movie, UserVisit


admin.site.register(User)
admin.site.register(Collection)
admin.site.register(Movie)
admin.site.register(UserVisit)