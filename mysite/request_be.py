from catalog.models import Produit
from qrcodes.models import codeqr
from achats.models import achats
from points.models import points
from django.contrib.auth.models import User
from django.db.models import Sum
from events.models import events
from .discord import *
from stockavatar.models import Stock
from histodefis.models import histodinos
from django.contrib.auth import get_user_model
from datetime import datetime

def get_x_prems():
    classement = points.objects.all()
    compteur = 1
    rep=[]
    for j in classement:
        dic = {}
        dic['surnom'] = j.surnom
        try :
            achatsss = achats.objects.filter(user=j.surnom).aggregate(Sum('prix'))
            if Stock.objects.filter(surnom=j.surnom).exists():
                dinos = Stock.objects.filter(surnom=j.surnom).count()
                dic['point'] = j.point + achatsss['prix__sum'] + dinos*2
            else :
                dic['point'] = j.point + achatsss['prix__sum']
        except :
            dic['point'] = j.point
        dic['avatar'] = j.avatar
        rep.append(dic)
    rep = sorted(rep, key=lambda d: d['point'], reverse=True)[:8]
    for i in rep:
        i['position']=compteur
        compteur +=1
    return rep

def get_shop(n,modulo):
    html = ""
    for j in Produit.objects.all()[n*modulo:(n+1)*modulo]:
        link = "/static/images/" + str(j.image)
        if j.price == 0:
            red = "/"
            button = "A gagner"
            prix ="Pas à vendre"
        else : 
            red = '/validate/' + str(j.id)
            prix = j.price 
            button = """ <svg width="24px" height="24px" viewBox="0 0 24.00 24.00" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M4.78571 5H18.2251C19.5903 5 20.5542 6.33739 20.1225 7.63246L18.4558 12.6325C18.1836 13.4491 17.4193 14 16.5585 14H6.07142M4.78571 5L4.74531 4.71716C4.60455 3.73186 3.76071 3 2.76541 3H2M4.78571 5L6.07142 14M6.07142 14L6.25469 15.2828C6.39545 16.2681 7.23929 17 8.23459 17H17M17 17C15.8954 17 15 17.8954 15 19C15 20.1046 15.8954 21 17 21C18.1046 21 19 20.1046 19 19C19 17.8954 18.1046 17 17 17ZM11 19C11 20.1046 10.1046 21 9 21C7.89543 21 7 20.1046 7 19C7 17.8954 7.89543 17 9 17C10.1046 17 11 17.8954 11 19Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg> """
        html += """
    <div class="content">
        <img src="{url}">
        <h3>{product}</h3>
        <p>{Description}</p>
        <h6>{prix} </h6>
        <button  class="buy-1" onClick="location.href='{link}'" type="button"> {button} </button>
    </div>
    """.format(url=link,product=j.title,Description=j.description,prix=prix, link = red,button = button )
    #"{% static '" + str(j.image)[7:] +  "' %}"
    return html


import qrcode 
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import csv
import os

import string
import random

BDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Logo_link = os.path.join(BDIR, 'images/logo.png')
L=12

def nom_alea(L):
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=L))

from django.urls import resolve
def gen_qrcode(montant,request):
    cle = nom_alea(L)
    while codeqr.objects.filter(code=cle).exists():
        cle = nom_alea(L)    
    url = 'https://jura7park.fr/validateqrcode/' + cle
    #Generate the QR code
    logo = Image.open(Logo_link)
    basewidth = 100
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(url)
    QRcode.make()
    QRcolor = 'Green'
    QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGB') 
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    namee = os.path.join(BDIR, 'staticfiles/pqrcodes/'+cle+'.png')
    QRimg.save(namee)

    #Write on the bottom white image
    #Open the white image
    img = Image.open('images/white.png')
    #Creation of the drawing
    d1 = ImageDraw.Draw(img)
    fontlink = os.path.join(BDIR, 'static/font/epilogue.ttf')
    font = ImageFont.truetype(fontlink, 40)
    font2 = ImageFont.truetype(fontlink, 30)  
    #Write the text
    d1.text((int(img.width/3)-5,20), str(montant) + ' points', fill=(0,0,0), font=font, align ="right")
    d1.text((20,img.height-50), 'Jura7Park', fill=(0,0,0), font=font2, align ="left")
    img.save('images/white2.png')

    #Open the images
    img = Image.open(namee)
    white = Image.open('images/white2.png')
    white = white.resize((img.width, int(img.height/2)))
    # Concatenate images
    img2 = Image.new("RGB",  (img.width,img.height+white.height))
    img2.paste(img, (0, 0))
    img2.paste(white, (0, img.height))
    img2.save(namee)
    print('QR code generated :', namee)
    return cle

#### EMAIL CUSTOM AFTER SHOP AND CODE


def code_exists(name2):
    if codeqr.objects.filter(code=name2).exists():
        return True
    else:
        return False

def code_used(name2,user):
    if codeqr.objects.filter(code=name2,utilisateur=user).exists():
        return True
    else :
        return False

def save_new_code(points, request, code,nb):
    title = str(points) + ' points'
    link = 'https://jura7park.fr/static/pqrcodes/'+code+'.png'
    codeqr.objects.create(code=code, createur = request.user, utilise=False, points=points, title=title,nb_utilisation = nb,lien = link)
    return True

def get_code_balance(code):
    try :
        code_current = codeqr.objects.get(code=code,utilise=False)
    except:
        return 0
    return code_current.points


def update_balance(user, pointss):
    try :
        userc = points.objects.get(surnom=user)
        userc.point += pointss
        userc.save()
    except :
        blaze= gen_nom_dino()
        points.objects.create(surnom=user, point=pointss, avatar = "mono.gif",nomavatar = blaze)
        add_avatar(user,blaze,"mono.gif")
    
from django.utils import timezone

def use_code(user, code):
    #Database update
    code_current = codeqr.objects.get(code=code, utilise=False)
    code_current.dateutil = timezone.now()
    code_current.nb_utilisation -= 1
    code_cree = codeqr.objects.create(
            code = code,
            dateutil = timezone.now(),
            utilisateur = user,
            points = code_current.points,
            utilise = True,
            createur = code_current.createur,
            title = code_current.title,
            nb_utilisation = 0,)
    code_cree.save()
    code_current.save()
    #Update balance
    update_balance(user, code_current.points)
    try :
    #Delete the QR code
        BDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.remove(os.path.join(BDIR, 'static\\pqrcodes\\' + code + '.png'))
    except:
        print('QR code not found'+str(code))

def get_stock(name):
    return Produit.objects.get(id=name).stock

def define_buying(name, user, points):
    #Update stock
    Produit.objects.filter(id=name).update(stock=int(get_stock(name))-1)
    #Update balance
    update_balance(user, -points)
    #Register the transaction
    achats.objects.create(user=user, produit=Produit.objects.get(id=name), prix=points)

def get_balance(user):
    try :
        pt = points.objects.get(surnom=user).point
    except :
        blaze = gen_nom_dino()
        points.objects.create(surnom=user, point=10, avatar = "mono.gif", nomavatar = blaze )
        add_avatar(user,blaze,"mono.gif")
        pt=10
    return pt

def get_recent_buyings(user):
    return achats.objects.filter(user=user).order_by('-date')

def get_recent_buyings2(user):
    return achats.objects.filter(user=user).order_by('-date')[:3]

def get_recent_qrcode(user):
    return codeqr.objects.filter(utilisateur=user).order_by('-dateutil')[:3]

def get_recent_qrcode2(user):
    return codeqr.objects.filter(utilisateur=user).order_by('-dateutil')

def get_price(name2):
    return Produit.objects.get(id=name2).price

def set_admin(username):
    user = User.objects.get(username=username)
    user.is_staff = True
    user.is_superuser = True
    user.save()

def set_staff(username):
    user = User.objects.get(username=username)
    user.is_staff = True
    user.save()
    
def unset_admin(username):
    user = User.objects.get(username=username)
    user.is_staff = False
    user.save()
    
    
dinos = ['Tyrannosaurus', 'Velociraptor', 'Stegosaurus', 'Triceratops', 'Brachiosaurus', 'Allosaurus', 'Ankylosaurus', 'Dilophosaurus', 'Parasaurolophus', 'Pterodactyl']
adjectifs = ['Epique', 'Légendaire', 'de TVN7','de Net7','de Can7','de Photo7','de Hi7Haut','de Ram7II','du Cartel','de Brew7','Trous Balourds','Sun7','de Moi7neuses Batteuse','Commun','Etrange','SN','MFEE','3EA','Etonnant','Enorme','Faineant','Fou','Génial','Gentil','Gros','Habile','Héroïque','Honnête','Imaginatif','Intelligent','Joli','Lâche','Léger','Lourd','Malin','Marrant','Mauvais','Merveilleux','Mignon','de n7beats']


def gen_nom_dino():
    adjectif = random.choice(adjectifs)
    dinosaure = random.choice(dinos)
    return dinosaure + ' ' + adjectif

def get_main(jour,periode):
    if events.objects.filter(jour=jour,periode=periode).exists():
        rep = []
        for j in events.objects.all().filter(jour=jour,periode=periode):
            dic={}
            dic['nom']=j.nom
            dic['horaires']=j.horaires
            rep.append(dic)
        return rep
    else:
        return []
    

def check_user(user):
    try :
        string = points.objects.get(surnom=user).surnom
        special_characters = """!@#$%^&*()-+?_=,<>/"""
        if any(c in special_characters for c in string):
            send_message('Pseudo étrange'+string)
    except:
        None 


def add_avatar(user,blaze,choice):
    if not Stock.objects.filter(surnom=user, avatar = choice, nomavatar = blaze).exists():
        Stock.objects.create(surnom=user, avatar = choice, nomavatar = blaze)
    else :
        print('Avatar déjà existant')

def gen_avatar(user,n):    
    modulo = 3
    html = ""
    if Stock.objects.all().filter(surnom =user).exists():
        for j in Stock.objects.all().filter(surnom =user)[n*modulo:(n+1)*modulo]:
            link = "/static/gif/" + str(j.avatar)
            red = "/chooseavatar/" + str(j.id)
            html += """
        <div class="content">
            <img src="{url}">
            <h3>{product}</h3>
            <p>{Description}</p>
            <button  class="buy-1" onClick="location.href='{link}'" type="button"> {button} </button>
        </div>
        """.format(url=link,product=j.avatar.replace('.gif',''),Description=j.nomavatar, link = red, button = 'Sélectionner')
    return html


User = get_user_model()
def histodefi(request,blaze,defi,montant):
    payeur  = request.user
    benef = User.objects.get(username=blaze)
    if not histodinos.objects.filter(beneficaire=benef,defi=defi).exists():
        send_defi(payeur,benef,defi,montant)
        histodinos.objects.create(payeur=payeur,beneficaire=benef,montant=montant,defi=defi,date=datetime.now())
        return True
    return False

def get_recent_challenges(user):
    query = histodinos.objects.filter(beneficaire=user).order_by('-date')
    rep = []
    for i in query : 
      dic = {}
      dic['montant'] = str(i.montant)
      dic['defi'] = str(i.get_day_display())
      dic['date'] = str(i.date)[:-15]
      rep.append(dic)
    print(rep)
    return rep