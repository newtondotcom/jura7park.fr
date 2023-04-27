"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import django_cas_ng.views
from django.conf import settings
from django.views.static import serve
from . import views
from rest_framework import routers


from points.urls import router as points_router
router = routers.DefaultRouter()
router.registry.extend(points_router.registry)


urlpatterns = [
    #path('', views.index, name='index'),
    path('ping', views.ping, name='ping'),
    path('shop/<nb>', views.shop),
    path('ld',views.leaderboard),
    path('enigmes',views.enigmelist),
    path('enigme/<nb>',views.enigme),
    path('repenigme',views.repenigme),
    path('registerbet/<id>',views.registerbet),
    path('bet',views.tempo),
    path('revealdino',views.revealdino),
    path('remerciements', views.remerciements),
    ##admin panel
    path('admin/', admin.site.urls),
    ##where a user can log in to the website
    path('accounts/login/', django_cas_ng.views.LoginView.as_view(),name='cas_ng_login'),
    ##where a user can log out to the website
    path('accounts/logout/', django_cas_ng.views.LogoutView.as_view(),name='cas_ng_logout'),
    #path('api',include(router.urls)),
    path('photos', views.showphotos),
    ##where an admin can create a code qr
    path('createcodeqr',views.createcodeqr),
    ##where an admin shows the code qr created
    path('codeqrcreated',views.codeqrcreated),
    ##where a user can validate a buying 
    path('validate/<name>',views.validate),
    ##where a user sees that is buying is confirmed
    path('validatedbuying/<name2>',views.validatedbuying),
    ##where a user validates a code
    path('validateqrcode/<name>',views.validateqrcode),
    ##where a user sees that is qrcode is confirmed
    path('validatedqrcode/<name2>',views.validatedqrcode),
    ##my account page
    path('myaccount',views.my_account),
    
   
    path('', include('pwa.urls')),
    #path('',views.test),  
    
    path('offline', views.offline), 
    
    ##Where to register an user as a staff
    path('registerstaff/<name>',views.registerstaff),
    path('registeradmin/<name>',views.registeradmin),
    ##Where to unregister an user as a staff
    path('unregisterstaff/<name>',views.unregisterstaff),

    path('avatarlist/<nb>',views.genavatarlist),

    path('chooseavatar/<nb>',views.chooseavatar),

    path('resetbalance',views.resetbalance),
    
    path('ub/<blaze>/<points>/<defi>',views.ub),

    path('adjust/<blaze>/<points>/<raison>',views.adjust),

    path('achats',views.achats),

    path('codes',views.codes),

    path('defis',views.defis),

    path('paylundi',views.paylundi),

    path('paybet1/<winner>/<cote>',views.paybet1),

    path('paybet2/<winner>/<cote>',views.paybet2),
]



admin.site.site_header  =  "Jura7Park"  
admin.site.site_title  =  "Jura7Park Admin"
admin.site.index_title  =  "Welcome to Jura7Park Admin"

