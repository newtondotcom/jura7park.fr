from catalog.models import Produit
from qrcodes.models import codeqr
from achats.models import achats
from points.models import points
from django.contrib.auth.models import User
from django.db.models import Sum

def get_x_prems():
    classement = points.objects.all()
    compteur = 1
    rep=[]
    for j in classement:
        dic = {}
        dic['surnom'] = j.surnom
        try :
            achatsss = achats.objects.filter(user=j.surnom).aggregate(Sum('prix'))
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
            html += """
    <div class="content">
        <img src="{url}">
        <h3>{product}</h3>
        <p>{Description}</p>
        <h6>{prix}</h6>
        <button  class="buy-1" onClick="location.href='{link}'" type="button"> <svg width="24px" height="24px" viewBox="0 0 24.00 24.00" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M4.78571 5H18.2251C19.5903 5 20.5542 6.33739 20.1225 7.63246L18.4558 12.6325C18.1836 13.4491 17.4193 14 16.5585 14H6.07142M4.78571 5L4.74531 4.71716C4.60455 3.73186 3.76071 3 2.76541 3H2M4.78571 5L6.07142 14M6.07142 14L6.25469 15.2828C6.39545 16.2681 7.23929 17 8.23459 17H17M17 17C15.8954 17 15 17.8954 15 19C15 20.1046 15.8954 21 17 21C18.1046 21 19 20.1046 19 19C19 17.8954 18.1046 17 17 17ZM11 19C11 20.1046 10.1046 21 9 21C7.89543 21 7 20.1046 7 19C7 17.8954 7.89543 17 9 17C10.1046 17 11 17.8954 11 19Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg></button>
    </div>
    """.format(url="/static/images/" + str(j.image),product=j.title,Description=j.description,prix=int(j.price), link = '/validate/' + str(j.id))
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
    namee = os.path.join(BDIR, 'static/pqrcodes/'+cle+'.png')
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

def save_new_code(points, request, code,public):
    title = str(points) + ' points'
    link = 'https://jura7park.fr/static/pqrcodes/'+code+'.png'
    codeqr.objects.create(code=code, createur = request.user, utilise=False, points=points, title=title, is_public=public,lien = link)
    return True

def get_code_balance(code):
    if codeqr.objects.filter(code=code).count() > 1 :
        code_current = codeqr.objects.get(code=code,is_public = True)
    else :
        code_current = codeqr.objects.get(code=code)
    return code_current.points


def update_balance(user, pointss):
    try :
        userc = points.objects.get(surnom=user)
        userc.point += pointss
        userc.save()
    except :
        points.objects.create(surnom=user, point=pointss, avatar = "mono.gif")
    
from django.utils import timezone

def use_code(user, code):
    #Database update
    code_current = codeqr.objects.get(code=code)
    if code_current.is_public == False:
        code_current.utilise = True
        code_current.utilisateur = user
    else:
        code_current.utilise = False
        code_cree = codeqr.objects.create(
            code = code,
            dateutil = timezone.now(),
            utilisateur = user,
            points = code_current.points,
            utilise = True,
            createur = code_current.createur,
            title = code_current.title,
            is_public = False,
        )
        code_cree.save()
    code_current.dateutil = timezone.now()
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
    Produit.objects.filter(id=name).update(stock=get_stock(name)-1)
    #Update balance
    update_balance(user, -points)
    #Register the transaction
    achats.objects.create(user=user, produit=Produit.objects.get(id=name), prix=points)

def get_balance(user):
    try :
        pt = points.objects.get(surnom=user).point
    except :
        pt = points.objects.create(surnom=user, point=0, avatar = "mono.gif")
    return pt

def get_recent_buyings(user):
    rep= achats.objects.filter(user=user).order_by('-date')[:3]
    nom1 = rep[0].produit.nom
    link1 = rep[0].produit.id
    prix1 = rep[0].prix
    date1 = rep[0].date
    nom2 = rep[1].produit.nom
    link2 = rep[1].produit.id
    prix2 = rep[1].prix
    date2 = rep[1].date  
    nom3 = rep[2].produit.nom
    link3 = rep[2].produit.id
    prix3 = rep[2].prix
    date3 = rep[2].date    
    return [nom1, link1, prix1, date1, nom2, link2, prix2, date2, nom3, link3, prix3, date3]

def get_recent_buyings2(user):
    return achats.objects.filter(user=user).order_by('-date')[:3]

def get_recent_qrcode(user):
    return codeqr.objects.filter(utilisateur=user).order_by('-dateutil')[:3]

def get_price(name2):
    return Produit.objects.get(id=name2).price

def set_admin(username):
    user = User.objects.get(username=username)
    user.is_staff = True
    user.save()
    
def unset_admin(username):
    user = User.objects.get(username=username)
    user.is_staff = False
    user.save()
    
    
dinos = ['Tyrannosaurus', 'Velociraptor', 'Stegosaurus', 'Triceratops', 'Brachiosaurus', 'Allosaurus', 'Ankylosaurus', 'Dilophosaurus', 'Parasaurolophus', 'Pterodactyl']
adjectifs = ['Epique', 'Légendaire', 'de TVN7','de Net7','de Can7','de Photo7','de Hi7Haut','de Ram7II','du Cartel','de Brew7','Trous Balourds','Sun7','de Moi7neuses Batteuse','Commun','Etrange','SN','MFEE','3EA','Etonnant','Enorme','Faineant','Fou','Génial','Gentil','Gros','Habile','Héroïque','Honnête','Imaginatif','Intelligent','Joli','Lâche','Léger','Lourd','Malin','Marrant','Mauvais','Merveilleux','Mignon']


def gen_nom_dino():
    adjectif = random.choice(adjectifs)
    dinosaure = random.choice(dinos)
    return dinosaure + ' ' + adjectif