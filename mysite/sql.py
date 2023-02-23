from getpass import getpass
from mysql.connector import connect, Error
import random
from discord_webhook import DiscordWebhook
import time    

#webhook = DiscordWebhook(url='your webhook url', content='Webhook Message')
#response = webhook.execute()

import qrcode 
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import csv
import os

import string
import random

Logo_link = 'static/logo.png'

connection = connect(
        host="sql7.freemysqlhosting.net",
        user="sql7588844",
        password="3f6BhFC8Cl",
        port = 3306,
        database="sql7588844",
    )

L=6

###MARCHE
def get_leaderboard():  ##renvoie le contenu de la table users sous forme de code html
    select_movies_query = """SELECT surnom,point,urlavatar FROM users order by point desc LIMIT 5"""
    result=""
    with connection.cursor() as cursor:
        cursor.execute(select_movies_query)
        html = "<table>"
        html += "<tr>"
        for column in cursor.description:
            html += "<th>{}</th>".format(column[0])
        html += "</tr>"
        for row in cursor:
            html += "<tr>"
            for cell in row:
                html += "<td>{}</td>".format(cell)
            html += "</tr>"
        html += "</table>"
        #print(html)
        return (html)

#leaderboard = get_leaderboard()

###MARCHE
def get_shop():  ##renvoie le contenu de la table shop sous forme de code html
    select_movies_query = """SELECT * FROM shop"""
    html =""
    with connection.cursor() as cursor:
        cursor.execute(select_movies_query)
        answer = cursor.fetchall()
        for j in answer:
            temp = list(j)
            print(temp[1])
            html += """
    <div class="content">
        <img src="/static/{productnorm}">
        <h3>{product}</h3>
        <p>{Description}</p>
        <h6>{prix}€</h6>
        <button  class="buy-{num}" onClick="location.href='{url}'" type="button"> Acheter</button>
    </div>
    """.format(productnorm=temp[1]+'.png',product=temp[5].capitalize(),Description=temp[4],prix=temp[2],num=random.randint(1,3), url = '/validate/'+temp[1])

    #print(html)
    return html   

#shop = get_shop()

###MARCHE
def get_balance(user): ##prend en entrée le surnom de l'utilisateur et renvoie son solde de points
    query = """SELECT point FROM users WHERE surnom = '%s'""" % user
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(list(answer[0])[0])
    return list(answer[0])[0]

#balance = get_balance("ZDZQSd")

###MARCHE
def get_desc(product): ##prend en entrée le nom du produit et renvoie sa description
    query = """SELECT description FROM shop WHERE produit = '%s'""" % product
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(list(answer[0])[0])
    return list(answer[0])[0]

#desc = get_desc("watch")

###MARCHE
def get_id_from_name_product(name): ##prend en entrée le nom du produit et renvoie son id
    query = """SELECT id FROM shop WHERE produit = '%s'""" % name
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(list(answer[0])[0])
    return list(answer[0])[0]

#id = get_id_from_name_product("watch")

###MARCHE
def get_id_from_name_user(name): ##prend en entrée le surnom de l'utilisateur et renvoie son id
    query = """SELECT id FROM users WHERE surnom = '%s'""" % name
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    return list(answer[0])[0]

###MARCHE
def save_qrcode(points, nombdd, user):   ##prend en entrée le montant de points, le nom inscrit dans la bdd et le surnom du créateur du code
    query = """INSERT INTO qrcode (cle, datecreation, auteur, points, utilise) VALUES (%s, %s, %s, %s, %s)"""
    date = time.strftime('%Y-%m-%d')
    data = (nombdd, date, get_id_from_name_user(user), points, 0)
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        connection.commit()
    print("Code saved")


#save_qrcode(100, "test", "ZDZQSd")

###MARCHE
def get_id_product_from_qrcode(qrcode):  ##prend en entrée le nom du qrcode et renvoie l'id du produit associé
    query = """SELECT id FROM qrcode WHERE cle = '%s'""" % qrcode
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(answer[0][0])
    return list(answer[0])[0]

#id = get_id_product_from_qrcode("test")

###MARCHE
def get_stock(product):  ##prend en entrée l'id d'un produit et renvoie le stock restant
    query = """SELECT stock FROM shop WHERE id = %s""" % product
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
        print('Stock de ',product, ' = ',answer[0][0])
    return answer[0][0]

#stock = get_stock(232)

###MARCHE
def update_stock(product):  ##prend en entrée l'id d'un produit et décrémente son stock de 1
    query = """UPDATE shop SET stock = stock - 1 WHERE id = %s""" % product
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
    print("Stock updated")

#update_stock(232)

###MARCHE
def get_balance_qrcode(qrcode):  ##prend en entrée le nom du qrcode et renvoie le montant de points associé
    query = """SELECT points FROM qrcode WHERE cle = '%s'""" % qrcode
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(answer[0][0])
    return answer[0][0]

#bal= get_balance_qrcode("test")

###MARCHE
def use_code(nom_code,utilisateur):  ##prend en entrée le nom du code et le surnom de l'utilisateur qui l'utilise et le marque comme utilisé dans la base de donnnées si le stock est > 0
    user = get_id_from_name_user(utilisateur)
    date = time.strftime('%Y-%m-%d')
    query = """update qrcode set utilise = 1, id_util = %s, dateutil = '%s' WHERE cle = '%s' """ %(user , date , nom_code)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

#use_code("test", "ZDZQSd")

###MARCHE
def update_balance(user, points):  ##prend en entrée le surnom de l'utilisateur et le montant de points à ajouter et met à jour son solde
    query = """UPDATE users SET point = point + %s WHERE surnom = '%s'""" % (points, user)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

#update_balance("ZDZQSd", 100)

def qr_code_exist(nom_code):  ##prend en entrée le nom du code et renvoie 1 si le code existe et 0 sinon
    query = """SELECT COUNT(*) FROM qrcode WHERE cle = '%s'""" % nom_code
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(answer[0][0])
    return answer[0][0]

def nom_alea(L):
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=L))

def gen_qrcode_serv(points, user):  ##prend en entrée le nom du qrcode, le montant de points et le surnom de l'utilisateur qui le crée et génère le qrcode
    name_random = nom_alea(L)
    while qr_code_exist(name_random) > 0:
        name_random = nom_alea(L)
    save_qrcode(points, name_random , user)  ###montant, cle, user donc tab sous forme : [montant,user]
    url ='validate'
    gen_qrcode(name_random, points, url)
    save_qrcode(points, name_random, user)
    return 'http://127.0.0.1:5000/static/qrcodes/'+name_random+'.png'

def gen_qrcode(cle, montant, url):
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
    namee = 'static/qrcodes/'+ cle + '.png'
    QRimg.save(namee)

    #Write on the bottom white image
    #Open the white image
    img = Image.open('images/white.png')
    #Creation of the drawing
    d1 = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 40)
    font2 = ImageFont.truetype('arial.ttf', 20)  
    #Write the text
    d1.text((int(img.width/3)-10,20), str(montant) + ' points', fill=(0,0,0), font=font, align ="right")
    d1.text((20,img.height-20), 'Jura7Park', fill=(0,0,0), font=font2, align ="left")
    img.save('images/white2.png')

    #Open the images
    img = Image.open(namee)
    white = Image.open('images/white2.png')
    white = white.resize((img.width, int(img.height/2)))
    # Concatenate images
    img2 = Image.new("RGB",  (img.width,img.height+white.height))
    print(img.size)
    print(white.size)
    img2.paste(img, (0, 0))
    img2.paste(white, (0, img.height))
    img2.save(namee)
    print('QR code generated :', namee)

def get_commercial_name(nombdd):
    query = """SELECT Nom_comm FROM shop WHERE produit = '%s'""" % nombdd
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(answer[0][0])
    return answer[0][0]

   
def get_price(nombdd):
    query = """SELECT prix FROM shop WHERE produit = '%s'""" % nombdd
    with connection.cursor() as cursor:
        cursor.execute(query)
        answer = cursor.fetchall()
    print(answer[0][0])
    return answer[0][0]



#connection.close()