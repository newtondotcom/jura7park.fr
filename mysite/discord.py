from discord_webhook import DiscordWebhook, DiscordEmbed


def send_achat(name,prix,objet):
    url = 'WEBHOOK URL'
    message = str(name) + " a acheté " + str(objet) + " pour " + str(prix) + " points"
    webhook = DiscordWebhook(url=url,content=message)
    # you can set the color as a decimal (color=242424) or hex (color='03b2f8') number
    embed = DiscordEmbed(title='Achat de ' +  name, description= objet + ' pour '+ str(prix), color='03b2f8')
    # add embed object to webhook
    webhook.add_embed(embed)
    response = webhook.execute()
    
def send_qr(name,cle,point):
    url = 'WEBHOOK URL'
    message = str(name) + " a utilisé le code QR " + str(cle) + " pour " + str(point) + " points"
    webhook = DiscordWebhook(url=url,content=message)
    embed = DiscordEmbed(title='Activation de' + name, description='Code : '+cle+ ' qui rapporte '+ str(point), color='03b2f8')
    webhook.add_embed(embed)
    response = webhook.execute()
    
def send_message(message):
    url = 'WEBHOOK URL'
    webhook = DiscordWebhook(url=url,content=message)
    response = webhook.execute()

def send_defi(payeur,beneficiaire,defi,montant):
    url = 'WEBHOOK URL'
    message = str(payeur) + " a validé le défi " + str(defi) + " pour " + str(beneficiaire) + " avec "+ str(montant) + " points"
    webhook = DiscordWebhook(url=url,content=message)
    embed = DiscordEmbed(title='Validation du défi' + str(defi), description= str(montant) + " pour " + str(beneficiaire), color='03b2f8')
    webhook.add_embed(embed)
    response = webhook.execute()