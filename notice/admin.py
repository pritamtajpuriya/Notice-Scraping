from django.contrib import admin
from .models import *


# Register your models here.


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'belongs', 'date', 'file', 'category',)
    list_filter = ('date', 'category', 'belongs',)
    search_fields = ('title', 'content')
    date_hierarchy = 'date'
    ordering = ('date',)


admin.site.register(Notice, NoticeAdmin)
