#!usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from main.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active')
    search_fields = ('email', 'username')
    list_filter = ('last_login', )
    date_hierarchy = 'last_login'
    ordering = ('-id', )


admin.site.register(Users, UsersAdmin)
