# Generated by Django 3.1.13 on 2023-03-02 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('histodefis', '0004_auto_20230227_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histodinos',
            name='defi',
            field=models.CharField(choices=[('1', 'Rembobiner'), ('2', 'Jura7Staff'), ('3', "Dans la peau d'un dino"), ('4', 'Eruption'), ('5', 'Clean my house'), ('6', 'Dompteur de dinos'), ('7', 'Instagraaaow'), ('8', 'Pro jura7'), ('9', 'Cruta7'), ('10', 'Herbivore confirmé'), ('11', 'Fictif'), ('12', 'Indiana Jaune'), ('13', 'Photosaure'), ('14', 'Jura-N7'), ('15', 'Camouflage'), ('16', "Le cri d'amour"), ('17', 'Les Dinoms'), ('18', 'Dino Train'), ('19', 'Dino di Caprio'), ('20', 'Cringeausaure'), ('21', 'Dinorigolo'), ('22', 'Photodino'), ('23', 'Cri au dino'), ('24', 'Surviva7'), ('25', 'Sa place est dans le musée'), ('26', 'Participation Rallye Colloc')], max_length=2),
        ),
    ]