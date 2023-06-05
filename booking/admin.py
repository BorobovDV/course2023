from django.contrib import admin
from .models import *


class ActualFilmsAdmin(admin.ModelAdmin):
    list_display = ('idfilm', 'name', 'duration', 'poster', 'trailer', 'flag', 'price')
    list_display_links = ('name',)
    search_fields = ('flag',)


admin.site.register(ActualFilms, ActualFilmsAdmin)


class PlacesAdmin(admin.ModelAdmin):
    list_display = ('idsession', 'p1', 'p2', 'p3', 'p4', 'p5',
                                 'p6', 'p7', 'p8', 'p9', 'p10',
                                 'p11', 'p12', 'p13', 'p14', 'p15',
                                 'p16', 'p17', 'p18', 'p19', 'p20',
                                 'p21', 'p22', 'p23', 'p24', 'p25', )
    list_display_links = ('idsession',)
    search_fields = ('idsession',)


admin.site.register(Places, PlacesAdmin)


class RentAdmin(admin.ModelAdmin):
    list_display = ('idrent', 'idsession', 'iduser', 'place', 'buyflg',)
    list_display_links = ('idrent',)
    search_fields = ('iduser', 'buyflg')


admin.site.register(Rent, RentAdmin)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('idsession', 'date', 'time', 'hall', 'idfilm',)
    list_display_links = ('idsession', 'date')
    search_fields = ('idsession', 'date', 'time')


admin.site.register(Session, SessionAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'email', 'login', 'password', 'role',)
    list_display_links = ('userid', 'email', 'login', 'role')
    search_fields = ('userid', 'email', 'login',)


admin.site.register(User, UserAdmin)
