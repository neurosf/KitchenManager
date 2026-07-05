from django.db.models import fields
from django import forms 
from .models import *
import json

class Composantform(forms.ModelForm):
    
    class Meta:
        model=Composant
        fields="__all__"

class Cuisineform(forms.ModelForm):
    
    class Meta:
        model=Cuisine
        fields=['Nom', 'Prix_achat', 'Prix_vente', 'quantite']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Prix_achat'].widget.attrs['readonly'] = True
        self.fields['Prix_vente'].widget.attrs['readonly'] = True

class Commandeform(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'  
        widgets = {
            'Mode_paiment': forms.Select(choices=[('par tranche', 'par tranche'), ('cash', 'cash')],
                                         attrs={'class': 'custom-select w-50'}),
            'deliver': forms.Select(choices=[(True,'livrer' ), (False,'ñ\'est pas livrer')],
                                         attrs={'class': 'custom-select w-50'}),
            'Date_comm': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cuisines = Cuisine.objects.all()
        # Add an empty option to the Cuisine field
        self.fields['Cuisine'].empty_label = "Select Cuisine"

        # Create a custom attribute data-cuisines with JSON data for each Cuisine option
        cuisines_data = [{'pk': c.pk, 'Nom': c.Nom, 'Prix_vente': c.Prix_vente} for c in cuisines]
        self.fields['Cuisine'].widget.attrs['data-cuisines'] = json.dumps(cuisines_data)
        
class CommandeCuisineForm(forms.ModelForm):
    Nom = forms.CharField(max_length=200)
    Prix_achat = forms.FloatField()
    Prix_vente = forms.FloatField()
    quantite = forms.FloatField()

    class Meta:
        model = Commande
        fields = ['Nom_Client', 'prenom_Client', 'Num_tele', 'Prix_commande', 'Prix_Paye', 'Date_comm', 'Mode_paiment', 'Nom', 'Prix_achat', 'Prix_vente', 'quantite']

        widgets = {
            'Mode_paiment': forms.Select(choices=[('par tranche', 'par tranche'), ('cash', 'cash')],
                                         attrs={'class': 'custom-select'}),
            'Cuisine': forms.Select(choices=[(c.pk, c.Nom) for c in Cuisine.objects.all()],
                        attrs={'class': 'custom-select'}),
        }

class Element_cuisineForm(forms.ModelForm):

    class Meta:
        model=Element_cuisine
        fields="__all__"
        widgets = {
            'Element': forms.Select(attrs={'class': 'custom-select'}),
        }

class Elementform(forms.ModelForm):
    
    class Meta:
        model=Element
        fields=['Nom', 'Prix_achat', 'Prix_vente', 'quantite','seuil','type']
        widgets = {
            'type': forms.Select(choices=[('construit', 'construit'), ('achetée', 'achetée')],attrs={'class': 'custom-select w-50'}),
        }

class Composant_ElementForm(forms.ModelForm):

    class Meta:
        model=Composant_Element
        fields="__all__"
        widgets = {
            'Quantite': forms.TextInput(attrs={'class': 'input-quantite w-100 p-1', 'placeholder': 'Quantite'}),
            'composant': forms.Select(attrs={'class': 'custom-select composantSelect'}),
        }

