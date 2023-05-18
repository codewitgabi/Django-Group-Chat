from django.contrib import admin
from .models import Group, Category, Message


class GroupAdmin(admin.ModelAdmin):
	list_display = ("name", "creator", "category")
	list_filter = ("category", "creator")
	search_fields = ("name",)


admin.site.register(Group, GroupAdmin)
admin.site.register(Category)
admin.site.register(Message)