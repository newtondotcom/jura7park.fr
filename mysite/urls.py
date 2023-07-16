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
from django.views.generic import TemplateView


from points.urls import router as points_router
router = routers.DefaultRouter()
router.registry.extend(points_router.registry)


urlpatterns = [
    ##where a user can log in to the website
    path('accounts/login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    ##where a user can log out to the website
    path('accounts/logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    
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

    ##Where to register an user as a staff
    path('registerstaff/<name>',views.registerstaff),
    ##Where to register an user as a admin
    path('registeradmin/<name>',views.registeradmin),
    ##Where to unregister an user as a staff
    path('unregisterstaff/<name>',views.unregisterstaff),
    ##Show the page nb of saved avatars
    path('avatarlist/<nb>',views.genavatarlist),
    ##Define the current avatar
    path('chooseavatar/<nb>',views.chooseavatar),
    ##Reset balance
    path('resetbalance',views.resetbalance),
    ##Update the balance of the user blaze with the value points for the reason defi
    path('ub/<blaze>/<points>/<defi>',views.ub),
    ##Adjust the balance of the user blaze with the value points for the reason raison
    path('adjust/<blaze>/<points>/<raison>',views.adjust),
    ##Shows the buying list
    path('achats',views.achats),
    ##Shows the qrcode list
    path('codes',views.codes),
    ##Shows the qrcode list
    path('defis',views.defis),
    ##Pay Monday Bet
    path('paylundi',views.paylundi),
    ##Pay users for bet n1
    path('paybet1/<winner>/<cote>',views.paybet1),
    ##Pay users for bet n2
    path('paybet2/<winner>/<cote>',views.paybet2),
    
    ###Notifications
    path('webpush/', include('webpush.urls')),
    path('testnotif', views.testnotif),
    path('sendnotif', views.sendnotif),
    #path('sw.js', TemplateView.as_view(template_name='slistener.js', content_type='application/x-javascript')),

    ###PWA
    path('offline', views.offline), 
    
    ###MUST BE AT THE END
    path('', include('pwa.urls')),
    
]



admin.site.site_header  =  "Jura7Park"  
admin.site.site_title  =  "Jura7Park Admin"
admin.site.index_title  =  "Welcome to Jura7Park Admin"

