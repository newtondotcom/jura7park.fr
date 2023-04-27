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
from qrcodes.models import codeqr
from paris.models import paris
from django.db.models import Sum,F
from photos.models import Photo
from repenigmes.models import repenigmes
from events.models import events
from django.contrib.auth import get_user_model


def message_error(message,url,bouton,request):
    context = { "message" : message, "url" : url , "bouton" : bouton}
    return render(request, 'err.html' , context = context)


def ping(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
      return HttpResponse('pong', content_type="text/plain")
    else:
      return HttpResponse('login', content_type="text/plain")


def shop(request,nb):
  number = Produit.objects.count()
  modulo = 3
  string = ""
  for i in range(number//3+1):
    string += """<a class="cgmtpage" href="/shop/0"""+str(i)+'">'+str(i+1)+'</a>\n'
  return render(request, 'shop.html',{"tab" : get_shop(int(nb),modulo),"string":string})

def test(request):
  if str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 3, 3))[:11] or True:
    parisss = """
      <div class="flex flex-col items-center justify-center">
    <a href="bet"><img src="/static/images/bet.svg" class="menuim"></a>
    <p class="paragraph">Paris dino</p>
  </div>
    """
    matin = get_main(5,1)
    midi = get_main(5,2)
    aprem = get_main(5,3)
    soir = get_main(5,4)
  else:
    parisss = ""
  if str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 25))[:11] or str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 24))[:11]:
    matin = get_main(6,1)
    midi = get_main(6,2)
    aprem = get_main(6,3)
    soir = get_main(6,4)
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 26))[:11]:
    matin = get_main(7,1)
    midi = get_main(7,2)
    aprem = get_main(7,3)
    soir = get_main(7,4)
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 27))[:11]:
    matin = get_main(1,1)
    midi = get_main(1,2)
    aprem = get_main(1,3)
    soir = get_main(1,4)
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 2, 28))[:11]:
    matin = get_main(2,1)
    midi = get_main(2,2)
    aprem = get_main(2,3)
    soir = get_main(2,4)
  
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 3, 1))[:11]:
    matin = get_main(3,1)
    midi = get_main(3,2)
    aprem = get_main(3,3)
    soir = get_main(3,4)
    
  elif str(datetime.datetime.now())[:11]==str(datetime.datetime(2023, 3, 2))[:11]:
    matin = get_main(4,1)
    midi = get_main(4,2)
    aprem = get_main(4,3)
    soir = get_main(4,4)
    
  return render(request,'indexe2.html', {"paris" : parisss,"matins":matin,"midi":midi,"aprem":aprem,"soir":soir})


def tempo(request):
  mt = paris.objects.all().aggregate(Sum('mise'))['mise__sum']
  if mt == None:
    mt = 0
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
    context = { "objet" : objet ,  "url" : url ,  "prix" : int(prix), "id" : name , "stock" : stock}
    return render(request, 'validate_buying.html', context = context)


def validatedbuying(request,name2):
  if not request.user.is_authenticated:
    message = "Vous devez etre connectes pour acheter un objet"
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
      message = "Vous devez etre connectes pour utiliser un code QR"
      url = "/accounts/login/"
      bouton = "Se connecter"
      return message_error(message,url,bouton,request)
  else:
    if code_exists(name2):
      if code_used(name2,request.user): 
        return message_error("Vous avez deja utilise ce code","/","Retour a l'accueil",request)
      elif codeqr.objects.filter(code=name2,utilise=False).get().nb_utilisation==0 or codeqr.objects.filter(code=name2,utilisateur=request.user).exists():
        return message_error("Ce code a deja ete utilise",'/','Retour a l\'accueil',request)
      else:
        prix = get_code_balance(name2)
        use_code(request.user, name2);
        send_qr(request.user.username, name2, prix)
        string = 'Ton code de ' + str(prix) + ' os est a toi, merci a toi ! ROOOOOARARR'
        return message_error(string,'/','Retour a l\'accueil',request)
    else:
        message = """Ce code n'existe pas, t'essaierais pas de nous douiller par hasard ?  <font size="5"> </h1> <h1>(ps : attention net𝟟, on vous surveille) </font>"""
        url = "/"
        bouton = "Retour a l'accueil"
        return message_error(message,url,bouton,request)


def enigme(request,nb):
  if not request.user.is_authenticated:
    return message_error("Vous devez etre connectes pour acceder a cette page",'/accounts/login/','Se connecter',request)
  else:
    if Enigme.objects.filter(user=request.user, numero_enigme=nb, is_valid=True).exists():
      indice = repenigmes.objects.filter(numero_enigme=nb).get().indice
      return message_error('Vous avez deja resolu cette enigme <font size="5"> </h1> <h1> Indice debloque : ' + str(indice) +""" </font>  """,'/enigmes','Retour aux énigmes',request)    
    context = {"Xok" : nb }
    return render(request, 'enigme.html', context = context)



def repenigme(request):
  rep = request.GET.get('reponse')
  day = request.GET.get('jour')
  answer = repenigmes.objects.get(numero_enigme=day).reponse
  if Enigme.objects.filter(user=request.user, numero_enigme=day, is_valid=True).exists():
    return message_error("Vous avez deja resolu cette enigme",'/enigmes','Retour aux énigmes',request)
  else:
    if str(rep.lower()).replace('é','e').replace('è','e').replace('à','a').replace(',',' ').replace('.', ' ').replace('ï','i').replace('â','a').replace('ê','e').replace('ô','o').replace(' ','') == str(answer):
      Enigme.objects.create(user=request.user, numero_enigme=day, reponse=rep, is_valid=True)
      update_balance(request.user, 10)
      return message_error("Bravo, ton indice apparait la ou tu viens de répondre! (et + dix os en cadeau)",'/enigmes','Retour a l\'accueil',request)
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
    return message_error("Vous devez etre connectes pour acceder a cette page",'/accounts/login/','Se connecter',request)
  else:
    montant = 2
    if int(get_balance(request.user)) >= montant:
      choice = weighted_random_by_dct(probas)
      blaze = gen_nom_dino()
      while Stock.objects.filter(surnom=request.user,avatar=choice,nomavatar=blaze).exists() :
        choice = weighted_random_by_dct(probas)
        blaze = gen_nom_dino()
      user = points.objects.get(surnom=request.user)
      user.avatar=choice
      user.nomavatar = blaze
      user.point = user.point - montant
      user.save()
      add_avatar(request.user,blaze,choice)
      avatar = points.objects.get(surnom=request.user).avatar
      return render(request, 'reveal_dino.html', {"avatar": avatar,"blaze":blaze})
    else: 
      return message_error("Tu n'as pas assez d'argent",'/',"Retour a l\'accueil",request)
  

def registerbet(request,id):
  montant = request.GET.get('bet')
  valeurrouge = request.GET.get('Rouge')
  valeurbleue = request.GET.get('Bleu')
  if not request.user.is_authenticated:
    return message_error("Vous devez etre connectes pour acceder a cette page",'/accounts/login/','Se connecter',request)
  else :
    if get_balance(request.user) < float(montant):
      return message_error("Vous n'avez pas assez d'argent pour effectuer cette transaction",'/','Retour a l\'accueil',request)
    elif paris.objects.filter(user=request.user,numero=id).exists():
      return message_error("Vous avez deja effectue un pari ;)",'/bet','Retour aux paris',request)
    elif float(montant) > 20:
      return message_error("Vous ne pouvez pas miser plus de 20 os",'/bet','Retour aux paris',request)
    else :
      if valeurrouge == "Rouge":
        on = 1
      elif valeurbleue == "Bleu":
        on = 2
      paris.objects.create(user=request.user, mise=montant, gagnant=on, numero=id)
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
  nb = request.GET.get('nb')
  cle = gen_qrcode(query,request)
  url = '/static/pqrcodes/'+cle+'.png'
  if save_new_code(query, request, cle,nb):
    return render(request, 'code_created.html', {"url" : url})
  else : 
    message = "Erreur lors de la creation du code, essayez a nouveau ou contactez un administrateur"
    url = "/createcodeqr"
    bouton = "Retour a l'accueil"
    return message_error(message,url,bouton,request)

def my_account(request):
  if request.user.is_authenticated:
    check_user(request.user)
    solde = get_balance(request.user)
    recent_buyings = get_recent_buyings2(request.user)
    recent_qrcode = get_recent_qrcode(request.user)
    req = points.objects.get(surnom=request.user)
    recent_challenges = histodinos.objects.all().filter(beneficaire=request.user).order_by('-date')[:3]
    avatar = req.avatar
    nomavatar = req.nomavatar
    rep=[]
    for i in recent_challenges:
      dic = {}
      dic['montant'] = str(i.montant)
      dic['defi'] = str(i.get_day_display())
      dic['date'] = str(i.date)[:-9]
      rep.append(dic)
    context = { "solde" : solde,
                "recent_buyings" : recent_buyings,
                "recent_qrcode" : recent_qrcode, 
                "avatar" : avatar,
                "nomavatar":nomavatar , 
                "recent_challenges" : rep }
    return render(request, 'my_account.html',context)
  else:
    return message_error("Vous devez etre connectes pour acceder a votre compte",'/accounts/login/','Se connecter',request)
  
@staff_member_required
def registerstaff(request,name):
  set_staff(name)
  send_message(str(name)+'a été mis staff par '+ str(request.user))
  #message_error("Vous avez bien ajoute " + name + " en tant qu'administrateur",'/admin','Retour a l\'accueil',request)
  return redirect('/admin/auth/user/')

@staff_member_required
def registeradmin(request,name):
  set_admin(name)
  send_message(str(name)+'a été mis staff par '+ str(request.user))
  #message_error("Vous avez bien ajoute " + name + " en tant qu'administrateur",'/admin','Retour a l\'accueil',request)
  return redirect('/admin/auth/user/')
  
@staff_member_required
def unregisterstaff(request,name):
  unset_admin(name)
  #message_error("Vous avez bien ajoute " + name + " en tant qu'administrateur",'/admin','Retour a l\'accueil',request)
  return redirect('/admin/auth/user/')

def genavatarlist(request,nb):
  if not request.user.is_authenticated:
    return message_error("Vous devez etre connectes pour acceder a cette page",'/accounts/login/','Se connecter',request)
  else:
    number = Stock.objects.filter(surnom=request.user).count()
    modulo = 3
    string = ""
    if not number<=3:
      for i in range(number//3+1):
        string += """<a class="cgmtpage" href="/avatarlist/"""+str(i)+'">'+str(i+1)+'</a>\n'
    return render(request, 'shop.html',{"tab" : gen_avatar(request.user,int(nb)),"string":string})
  
def chooseavatar(request,nb):
  curruser = request.user
  avatarselected = Stock.objects.get(id=nb)
  query = points.objects.get(surnom=curruser)
  query.avatar = avatarselected.avatar
  query.nomavatar = avatarselected.nomavatar
  query.save()
  return message_error("Vous avez bien choisi votre avatar !",'/myaccount','Retour sur ton profil',request)
    
@staff_member_required
def resetbalance(request):
  for i in points.objects.all():
    try :
      query = Stock(avatar = i.avatar,nomavatar = i.nomavatar,surnom = i.surnom)
      query.save()
    except :
      None
  for i in points.objects.all():
    i.point = 10
    if codeqr.objects.filter(utilisateur=i.surnom,utilise=True).exists():
      for j in codeqr.objects.all().filter(utilisateur=i.surnom,utilise=True):
        i.point += j.points
    i.save()
  return message_error("Les balances ont bien ete remises a zero !",'/admin/','Retour a l\'accueil',request)

@staff_member_required
def ub(request,blaze,points,defi):
  User = get_user_model()
  user = User.objects.get(username=blaze)
  if histodefi(request,blaze,defi,points):
    update_balance(user,int(points))
    return message_error("Thune ajoutée !",'/admin/','Retour a l\'accueil',request)
  else :
    return message_error("Défi déjà complété",'/admin/','Retour a l\'accueil',request)

@staff_member_required
def adjust(request,blaze,points,raison):
  User = get_user_model()
  user = User.objects.get(username=blaze)
  update_balance(user,int(points))
  send_message("L'administrateur "+str(request.user)+" a modifié le solde de "+str(blaze)+" de "+str(points)+" points pour la raison suivante : "+str(raison))
  return message_error("Solde modifié !",'/admin/','Retour a l\'accueil',request)


def achats(request):
  recent_buyings = get_recent_buyings(request.user)
  return render(request, 'details.html',{"recent_buyings":recent_buyings})

def codes(request):
  recent_qrcode = get_recent_qrcode2(request.user)
  return render(request, 'details_codes.html',{"recent_qrcode":recent_qrcode})

def defis(request):
  recent_challenges = get_recent_challenges(request.user)
  return render(request, 'details_defis.html',{"recent_challenges":recent_challenges})

@staff_member_required
def paylundi(request):
  day = 1
  query = Enigme.objects.all().filter(numero_enigme=day, is_valid=True)
  for i in query:
    update_balance(i.user,10)
  return message_error("Les paris de lundi ont bien ete payes !",'/admin/','Retour a l\'accueil',request)


@staff_member_required
def paybet1(request,winner,cote):
  parisss = paris.objects.all().filter(numero=1)
  for i in parisss: 
    if not i.is_paid:
      if str(i.gagnant) == (winner) :
        update_balance(request.user,round(i.mise*float(cote)))
      i.is_paid = True
      i.save()
  return message_error("Les paris ont bien ete payes !",'/admin/','Retour a l\'accueil',request)


@staff_member_required
def paybet2(request,winner,cote):
  parisss = paris.objects.all().filter(numero=2)
  for i in parisss: 
    if not i.is_paid:
      if str(i.gagnant) == (winner) :
        update_balance(request.user,round(i.mise*float(cote)))
      i.is_paid = True
      i.save()
  return message_error("Les paris ont bien ete payes !",'/admin/','Retour a l\'accueil',request)


####SQL REQUEST CODEQR le 26 : SELECT qrcodes_codeqr.dateutil,auth_user.username,sum(qrcodes_codeqr.points) , COUNT(*) FROM qrcodes_codeqr ,auth_user WHERE qrcodes_codeqr.utilisateur_id = auth_user.id and SUBSTR(qrcodes_codeqr.dateutil,9,2)= 26 group by auth_user.username HAVING COUNT(*)>2

def offline(request):
  return message_error("L'appli n'est pas connectée à Internet",'/','Désolé')