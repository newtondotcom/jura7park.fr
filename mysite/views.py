from django.http import HttpRequest, HttpResponse
from . import signals
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .request_be import *
from points.models import points
from django.contrib.admin.views.decorators import staff_member_required
from .discord import *
from enigmes.models import Enigme
import datetime
from paris.models import paris
from django.db.models import Sum,F
from photos.models import Photo
from repenigmes.models import repenigmes
from events.models import events


def message_error(message,url,bouton,request):
    context = { "message" : message, "url" : url , "bouton" : bouton}
    return render(request, 'err.html' , context = context)

def index(request: HttpRequest) -> HttpResponse:
    header = '''<!DOCTYPE html>
<html>
  <head>
    <title>django-cas-ng example demo</title>
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0, minimum-scale=1.0">
  </head>
  <body>
  <h1>Welcome to django-cas-ng demo</h1>'''

    footer = '''<p>Related post:</p>
    <ul>
        <li><a href="https://djangocas.dev/blog/django-cas-ng-example-project/">Step by step to setup a django-cas-ng example project</a></li>
    </ul>
    <hr><p><a href="https://djangocas.dev/">Project homepage</a></p>
  </body>
</html>'''

    if request.user.is_authenticated:
        body = """
        <p>You logged in as <strong>%s</strong>.</p>
        <p><a href="/accounts/logout">Logout</a></p>
         """ % request.user.username
    else:
        body = '<p><a href="/accounts/login/">Login</a></p>'

    return HttpResponse(header + body + footer)


def main(request: HttpRequest) -> HttpResponse:
    return HttpResponse('login', content_type="text/plain")

def ping(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
      return HttpResponse('pong', content_type="text/plain")
    else:
      return HttpResponse('login', content_type="text/plain")

def template(request):
  return render(request, 'main.html',{"message" : 'ls.message'})

def shop(request,nb):
  number = Produit.objects.count()
  modulo = 3
  string = ""
  for i in range(number//3+1):
    string += """<a class="cgmtpage" href="/shop/0"""+str(i)+'">'+str(i+1)+'</a>\n'
  return render(request, 'shop.html',{"tab" : get_shop(int(nb),modulo),"string":string})

def test(request):
  if str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 3, 3))[:11]:
    parisss = """
      <div class="flex flex-col items-center justify-center">
    <a href="bet"><img src="/static/images/bet.svg" class="menuim"></a>
    <p class="paragraph">Paris dino</p>
  </div>
    """
    matin = events.objects.filter(jour=5,periode=1).get()
    midi = events.objects.filter(jour=5,periode=2).get()
    aprem = events.objects.filter(jour=5,periode=3).get()
    soir = events.objects.filter(jour=5,periode=4).get()
  else:
    parisss = ""
  if str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 25))[:11] or str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 23))[:11]or str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 24))[:11]:
    matin = events.objects.filter(jour=6,periode=1).get()
    midi = events.objects.filter(jour=6,periode=2).get()
    aprem = events.objects.filter(jour=6,periode=3).get()
    soir = events.objects.filter(jour=6,periode=4).get()
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 26))[:11]:
    matin = events.objects.filter(jour=7,periode=1).get()
    midi = events.objects.filter(jour=7,periode=2).get()
    aprem = events.objects.filter(jour=7,periode=3).get()
    soir = events.objects.filter(jour=7,periode=4).get()
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 27))[:11]:
    matin = events.objects.filter(jour=1,periode=1).get()
    midi = events.objects.filter(jour=1,periode=2).get()
    aprem = events.objects.filter(jour=1,periode=3).get()
    soir = events.objects.filter(jour=1,periode=4).get()
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 28))[:11]:
    matin = events.objects.filter(jour=2,periode=1).get()
    midi = events.objects.filter(jour=2,periode=2).get()
    aprem = events.objects.filter(jour=2,periode=3).get()
    soir = events.objects.filter(jour=2,periode=4).get()
  
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 3, 1))[:11]:
    matin = events.objects.filter(jour=3,periode=1).get()
    midi = events.objects.filter(jour=3,periode=2).get()
    aprem = events.objects.filter(jour=3,periode=3).get()
    soir = events.objects.filter(jour=3,periode=4).get()
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 3, 2))[:11]:
    matin = events.objects.filter(jour=4,periode=1).get()
    midi = events.objects.filter(jour=4,periode=2).get()
    aprem = events.objects.filter(jour=4,periode=3).get()
    soir = events.objects.filter(jour=4,periode=4).get()
    
  return render(request,'indexe2.html', {"paris" : parisss,"matin":matin,"midi":midi,"aprem":aprem,"soir":soir})


def tempo(request):
  mt = paris.objects.all().aggregate(Sum('mise'))['mise__sum']
  return render(request, 'bet.html',{"mt":mt})

from .gen_ldb import *

def leaderboard(request):
  context = {"joueurs" :get_x_prems()}
  return render(request, 'leaderboard.html', context = context)

def validate(request,name):
  if not request.user.is_authenticated:
   return message_error("Vous devez etre connectes",'/accounts/login/','Se connecter',request)
  else:
    current_object = Produit.objects.get(id=name)
    objet = current_object.title
    url = "/static/images/" + str(current_object.image)
    prix =  current_object.price
    stock = current_object.stock
    context = { "objet" : objet ,  "url" : url ,  "prix" : prix, "id" : name , "stock" : stock}
    return render(request, 'validate_buying.html', context = context)


def validatedbuying(request,name2):
  if not request.user.is_authenticated:
    message = "Vous devez etre connecte pour acheter un objet"
    url = "/accounts/login/"
    bouton = "Se connecter"
    context = { "message" : message, "url" : url , "bouton" : bouton}
    return render(request, 'err.html' , context = context)
  else:
    if not int(get_balance(request.user)) < int(get_price(name2)):
      if get_stock(name2) > 0:
        current_object = Produit.objects.get(id=name2)
        ##BACK END
        prix = current_object.price
        define_buying(name2, request.user, prix)
        ##FRONT END
        objet = current_object.title
        prix = int(prix)
        url = "/static/images/" + str(current_object.image)
        print(url)
        context = { "objet" : objet ,  "url" : url ,  "prix" : prix}
        message = str(request.user.username) + " a achete " + str(objet) + " pour " + str(prix) + " points"
        send_achat(request.user.username, prix, objet)
        return render(request, 'buying_validated.html', context = context)
      else:
        return message_error("Il n'en reste plus assez, tout a ete mange",'/shop/0','Retour au shop',request)
    else:      
      return message_error("Vous n'avez pas assez d'os",'/shop/0','Retour au shop',request)

def validateqrcode(request,name):
  if not codeqr.objects.filter(code=name).exists():
    return message_error("""Ce code n'existe pas, t'essaierais pas de nous douiller par hasard ?  <font size="5"> </h1> <h1>(ps : attention net𝟟, on vous surveille) </font>""",'/','Retour a l\'accueil',request)
  prix = get_code_balance(name)
  context = { "prix" : prix, "key" : name}
  return render(request, 'validate_qrcode.html',context = context)

def remerciements(request):
  return render(request, 'thanks.html')

def validatedqrcode(request,name2):
  if not request.user.is_authenticated:
      message = "Vous devez etre connecte pour utiliser un code QR"
      url = "/accounts/login/"
      bouton = "Se connecter"
      return message_error(message,url,bouton,request)
  else:
    if code_exists(name2):
      ###CODE PUBLIC UTILISE
      if code_used(name2,request.user): 
        return message_error("Vous avez deja utilise ce code","/","Retour a l'accueil",request)
      ###CODE PRIVE UTILISE
      elif codeqr.objects.get(code=name2).is_public == False and codeqr.objects.get(code=name2).utilise :
        return message_error("Ce code a deja ete utilise",'/','Retour a l\'accueil',request)
      else:
        prix = get_code_balance(name2)
        use_code(request.user, name2);
        context = { "prix" : prix}
        send_qr(request.user.username, name2, prix)
        string = 'Ton code de ' + str(prix) + ' os, merci a toi ! ROOOOOARARR'
        return message_error(string,'/','Retour a l\'accueil',request)
    else:
        message = """Ce code n'existe pas, t'essaierais pas de nous douiller par hasard ?  <font size="5"> </h1> <h1>(ps : attention net𝟟, on vous surveille) </font>"""
        url = "/"
        bouton = "Retour a l'accueil"
        return message_error(message,url,bouton,request)


def enigme(request,nb):
  if not request.user.is_authenticated:
    return message_error("Vous devez etre connecte pour acceder a cette page",'/accounts/login/','Se connecter',request)
  else:
    if Enigme.objects.filter(user=request.user, numero_enigme=nb, is_valid=True).exists():
      indice = repenigmes.objects.filter(numero_enigme=nb).get().indice
      return message_error('Vous avez deja resolu cette enigme <font size="5"> </h1> <h1> Indice debloque :' + str(indice) +""" </font>  """,'/enigmes','Retour a l\'accueil',request)
    context = {"Xok" : nb }
    return render(request, 'enigme.html', context = context)



def repenigme(request):
  rep = request.GET.get('reponse')
  day = request.GET.get('jour')
  answer = repenigmes.objects.get(numero_enigme=day).reponse
  if str(rep.lower().replace('é','e').replace('è','e').replace('à','a').replace(',',' ').replace('.', ' ')) == str(answer):
    Enigme.objects.create(user=request.user, numero_enigme=day, reponse=rep, is_valid=True)
    return message_error("Bravo, tu as debloque un indice qui sera a la place de la question de ce jour !",'/','Retour a l\'accueil',request)
  else:
    return message_error("Mauvaise reponse, essaie encore !",'/enigmes','Retour a l\'enigme',request)


def enigmelist(request):
  return render(request, 'enigmelist.html')

probas = {"doux.gif":0.1,"kira.gif":0.1,"kuro.gif":0.1,"loki.gif":0.1,"mono.gif":0.1,"kuro.gif":0.1,"loki.gif":0.1,"mono.gif":0.1,"mort.gif":0.1,"nico.gif":0.1,"olaf.gif":0.1,"tard.gif":0.1,"vita.gif":0.1}

def weighted_random_by_dct(dct):
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
           
def revealdino(request):
  if not request.user.is_authenticated:
    return message_error("Vous devez etre connecte pour acceder a cette page",'/accounts/login/','Se connecter',request)
  else:
    montant = 2
    if int(get_balance(request.user)) >= montant:
      choice = weighted_random_by_dct(probas)
      blaze = gen_nom_dino()
      user = points.objects.get(surnom=request.user)
      user.avatar=choice
      user.nomavatar = blaze
      user.point = user.point - montant
      user.save()
      avatar = points.objects.get(surnom=request.user).avatar
      return render(request, 'reveal_dino.html', {"avatar": avatar,"blaze":blaze})
    else: 
      return message_error("Tu n'as pas assez d'argent",'/',"Retour a l\'accueil",request)
  

def registerbet(request):
  montant = request.GET.get('bet')
  valeurrouge = request.GET.get('Rouge')
  valeurbleue = request.GET.get('Bleu')
  if not request.user.is_authenticated:
    return message_error("Vous devez etre connecte pour acceder a cette page",'/accounts/login/','Se connecter',request)
  else :
    if get_balance(request.user) < float(montant):
      return message_error("Vous n'avez pas assez d'argent pour effectuer cette transaction",'/','Retour a l\'accueil',request)
    else :
      if valeurrouge == "Rouge":
        on = 1
      elif valeurbleue == "Bleu":
        on = 2
      paris.objects.create(user=request.user, mise=montant, gagnant=on)
      return message_error("Votre pari a bien ete enregistre !",'/','Retour a l\'accueil',request)


def showphotos(request):
  photos = Photo.objects.all()
  context = {'photos' : photos}
  return render(request, 'photos.html', context = context)

@staff_member_required
def createcodeqr(request):
  return render(request, 'gen_qr.html')

@staff_member_required
def codeqrcreated(request):
  query = request.GET.get('montant')
  if request.GET.get('public') == 'on':
    public = True
  else :
    public = False
  cle = gen_qrcode(query,request)
  url = '/static/pqrcodes/'+cle+'.png'
  if save_new_code(query, request, cle,public):
    return render(request, 'code_created.html', {"url" : url})
  else : 
    message = "Erreur lors de la creation du code, essayez a nouveau ou contactez un administrateur"
    url = "/createcodeqr"
    bouton = "Retour a l'accueil"
    return message_error(message,url,bouton,request)

def my_account(request):
  if request.user.is_authenticated:
    req = points.objects.get(surnom=request.user)
    avatar = req.avatar
    nomavatar = req.nomavatar
    solde = get_balance(request.user)
    recent_buyings = get_recent_buyings2(request.user)
    recent_qrcode = get_recent_qrcode(request.user)
    context = { "solde" : solde, "recent_buyings" : recent_buyings, "recent_qrcode" : recent_qrcode, "avatar" : avatar,"nomavatar":nomavatar }
    return render(request, 'my_account.html',context)
  else:
    return message_error("Vous devez etre connecte pour acceder a votre compte",'/accounts/login/','Se connecter',request)
  
@staff_member_required
def registerstaff(request,name):
  set_admin(name)
  send_message(str(name)+'a été mis staff par '+ str(request.user))
  #message_error("Vous avez bien ajoute " + name + " en tant qu'administrateur",'/admin','Retour a l\'accueil',request)
  return redirect('/admin/auth/user/')
  
@staff_member_required
def unregisterstaff(request,name):
  unset_admin(name)
  #message_error("Vous avez bien ajoute " + name + " en tant qu'administrateur",'/admin','Retour a l\'accueil',request)
  return redirect('/admin/auth/user/')

@staff_member_required
def paybets(request,winner,cote):
  parisss = paris.objects.all()
  for i in parisss: 
    if not i.is_paid:
      if str(i.gagnant) == (winner) :
        update_balance(request.user,round(i.mise*float(cote)))
      i.is_paid = True
      i.save()
  return message_error("Les paris ont bien ete payes !",'/admin/','Retour a l\'accueil',request)
  