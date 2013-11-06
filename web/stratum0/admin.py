from django.contrib import admin
from stratum0.models import Stratum1

class Stratum1Admin(admin.ModelAdmin):
	fields = ['url']
	list_display = ['url', 'stratum0_fqrn']
	list_filter = ['stratum0_fqrn']

admin.site.register(Stratum1, Stratum1Admin)
