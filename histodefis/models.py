from django.db import models

day_CHOICES = (
    ('1', 'Rembobiner'),
    ('2', 'Jura7Staff'),
    ('3', 'Dans la peau d\'un dino'),
    ('4', 'Eruption'),
    ('5', 'Clean my house'),
    ('6', 'Dompteur de dinos'),
    ('7', 'Instagraaaow'),
    ('8', 'Pro jura7'),
    ('9', 'Cruta7'),
    ('10', 'Herbivore confirmé'),
    ('11', 'Fictif'),
    ('12', 'Indiana Jaune'),
    ('13', 'Photosaure'),
    ('14', 'Jura-N7'),
    ('15', 'Camouflage'),
    ('16', 'Le cri d\'amour'),
    ('17', 'Les Dinoms'),
    ('18', 'Dino Train'),
    ('19', 'Dino di Caprio'),
    ('20', 'Cringeausaure'),
    ('21', 'Dinorigolo'),
    ('22', 'Photodino'),
    ('23', 'Cri au dino'),
    ('24', 'Surviva7'),
    ('25', 'Sa place est dans le musée'),
    ('26', 'Participation Rallye Colloc'),
    )

# Create your models here.
class histodinos(models.Model):
    defi = models.CharField(choices=day_CHOICES,max_length=2)
    beneficaire = models.ForeignKey('auth.User', related_name='benf',on_delete=models.CASCADE)
    montant = models.IntegerField()
    payeur = models.ForeignKey('auth.User', related_name='pay',on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)

    def get_day_display(self):
        return dict(day_CHOICES)[self.defi]