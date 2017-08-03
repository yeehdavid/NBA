from django.contrib import admin
from .models import Videos,Board_News,Board_Videos,Latest_News
admin.site.register(Board_Videos)
admin.site.register(Latest_News)
admin.site.register(Videos)
admin.site.register(Board_News)
# Register your models here.
