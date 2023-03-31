from django.contrib import admin

class BandAdmin(admin.ModelAdmin):  
    list_display = ('name', 'year_formed', 'genre') 

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'band')  
