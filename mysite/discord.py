from discord_webhook import DiscordWebhook, DiscordEmbed


def send_achat(name,prix,objet):
    url = 'https://discord.com/api/webhooks/1067118081425539122/t7xqlZtvFkV7902fQzI9x78fplhD9yVOR3G_LswoGcg6fewBeRO1E4Q12GJhkCxH8-Os'
    message = str(name) + " a acheté " + str(objet) + " pour " + str(prix) + " points"
    webhook = DiscordWebhook(url=url,content=message)
    # you can set the color as a decimal (color=242424) or hex (color='03b2f8') number
    embed = DiscordEmbed(title='Achat de ' +  name, description= objet + ' pour '+ str(prix), color='03b2f8')
    # add embed object to webhook
    webhook.add_embed(embed)
    response = webhook.execute()
    
def send_qr(name,cle,point):
    url = 'https://discord.com/api/webhooks/1067118038383599717/f0BN7dRCB7omflslGgUoJJH1u0_WLb7Z-kaOBijlQVShz2lzxTRi5VLVze6K5BUfVFkg'
    message = str(name) + " a utilisé le code QR " + str(cle) + " pour " + str(point) + " points"
    webhook = DiscordWebhook(url=url,content=message)
    embed = DiscordEmbed(title='Activation de' + name, description='Code : '+cle+ ' qui rapporte '+ str(point), color='03b2f8')
    webhook.add_embed(embed)
    response = webhook.execute()
    
def send_message(message):
    url = 'https://discord.com/api/webhooks/1078313459319590994/thxGGDNqfZinhkh5Yu98IKepLuiagCwCzlaeCRnqfGE6H8In1ET0IldaLUA_Dr2lyjWk'
    webhook = DiscordWebhook(url=url,content=message)
    response = webhook.execute()