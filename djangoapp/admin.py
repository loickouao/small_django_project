from django.contrib import admin


from .models import Stock, Price

# Register your models here.

class StockAdmin(admin.ModelAdmin):
    readonly_fields = ('price',)

admin.site.register(Stock)
admin.site.register(Price)

