from django.contrib import admin

from proxy.models import Proxy, Category


@admin.register(Proxy)
class Admin(admin.ModelAdmin):
    list_display = ["pk", "url", "amount"]
    list_display_links = list_display


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    list_display_links = list_display
