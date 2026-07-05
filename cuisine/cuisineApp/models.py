from django.db import models

class Element(models.Model):

    Nom = models.CharField(max_length=100)
    Prix_achat = models.FloatField(blank=True, null=True)
    Prix_vente = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=30)
    quantite = models.FloatField(default=0)
    seuil = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id}- {self.Nom} ({self.Prix_vente})"

class Cuisine(models.Model):

    Nom = models.CharField(max_length=200)
    Prix_achat = models.FloatField(default=0)
    Prix_vente = models.FloatField(default=0)
    quantite = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id}- {self.Nom} ({self.Prix_vente})"

class Element_cuisine(models.Model):

    Element = models.ForeignKey('Element',on_delete=models.CASCADE)
    Cuisin = models.ForeignKey('Cuisine',on_delete=models.CASCADE)
    Quantite = models.FloatField()

class Commande(models.Model):

    Nom_Client = models.CharField(max_length=100)
    prenom_Client = models.CharField(max_length=100)
    Num_tele = models.CharField(max_length=20,blank=True)
    Mode_paiment = models.CharField(max_length=20, choices=[('par tranche', 'par tranche'), ('cash', 'cash')])
    Prix_Transport = models.FloatField(default=0)
    Prix_commande = models.FloatField(default=0)
    Prix_Paye = models.FloatField(default=0)
    Date_comm = models.DateField()
    deliver = models.BooleanField(default=False,choices=[(True,'livrer' ), (False,'ñ\'est pas livrer')])
    Cuisine = models.ForeignKey('Cuisine',on_delete=models.SET_DEFAULT,default=0,null=True,blank=True)

class User(models.Model):

    UserName = models.CharField(max_length=100)
    PssWord = models.CharField(max_length=100)

class Composant(models.Model):

    Nom = models.CharField(max_length=100)
    Prix_achat = models.FloatField()
    quantite = models.FloatField()
    seuil = models.FloatField()
    Langeur = models.FloatField(blank=True, null=True)
    Largeur = models.FloatField(blank=True, null=True)

    def __str__(self):
        dimensions = f" ({self.Langeur}*{self.Largeur})" if self.Langeur is not None and self.Largeur is not None else ""
        return f"{self.id}- {self.Nom}{dimensions}"

class Composant_Element(models.Model):

    Element = models.ForeignKey('Element',on_delete=models.CASCADE)
    composant = models.ForeignKey('composant',on_delete=models.CASCADE)
    Quantite= models.FloatField()