import base64
from django.shortcuts import get_object_or_404, render ,redirect
from django.contrib import messages
from .Forms import *
from .models import *
import datetime
from datetime import date, datetime, timedelta
from django.db.models import Q,F
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
#import matplotlib.pyplot as plt
import io
# Create your views here.

def MainPage(request):
    if(LoginVerfication(request)==-1):return redirect('Login')
    return render(request, "index.html")

def loginPage(request):
    message = ""
    username = ""
    password = ""
    if datecondition()!=-1 :

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            V=User.objects.filter(UserName=username).exists()
            if V:
                user=User.objects.get(UserName=username)
                if user!=0:
                    if(user.PssWord== password):
                        expires = datetime.now() + timedelta (days=1)
                        encoded_credentials = encode_credentials(username, password)
                        response = redirect('main')
                        response.set_cookie('credentials', encoded_credentials, expires=expires)
                        return response
                    else:
                        message = "Mot de pas inccorect" 
            else: 
                message = "Utilisater n'esist pas"
    return render(request, "Login.html",{"message":message,'user':username,'password':password})

def LoginVerfication(request):
    if datecondition()==-1 :return -1
    encoded_credentials = request.COOKIES.get('credentials')

    if not encoded_credentials:
        return -1
    try:
        username, password = decode_credentials(encoded_credentials)
        user=User.objects.filter(Q(UserName=username)&Q(PssWord=password))
    except User.DoesNotExist:
        return -1
    if len(user)==0:
        return -1  

def datecondition():
    todaydate = datetime.now().date()
    cutoff_date = datetime(2023, 11, 18).date()

    if todaydate > cutoff_date: return -1
    
def Logout(request):
    return removeCookies(request)

def removeCookies(request):
    response = redirect('main') 
    response.delete_cookie('credentials') 
    return response

def encode_credentials(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return encoded_credentials

def decode_credentials(encoded_credentials):
    decoded_credentials = base64.b64decode(encoded_credentials.encode()).decode()
    username, password = decoded_credentials.split(':')
    return username, password

#########################
def composantPage(request):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreComposant = Composant.objects.all().count()
        Composantoseuil = Composant.objects.filter(seuil__gt=F('quantite'))
        formcomposant = Composantform()
        composant = Composant.objects.all()
        return  render(request, "composant.html", {"composant":composant,"NembreComposant":NembreComposant,"formcomposant":formcomposant,"Composantoseuil":Composantoseuil})
    if request.method == 'POST':
        form = Composantform(request.POST)
        if form.is_valid():
            form.save()
        return redirect('composant')

def composantEdit(request,id=0):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreComposant = Composant.objects.all().count()
        Composantoseuil = Composant.objects.filter(seuil__gt=F('quantite'))
        formcomposant = Composantform()
        Inst = get_object_or_404(Composant, id=id)
        selectedComposant = Composantform(instance=Inst)
        return  render(request, "composant.html", {"NembreComposant":NembreComposant,"formcomposant":formcomposant,"selectedComposant":selectedComposant,"Composantoseuil":Composantoseuil})
    if request.method == 'POST':
        Inst = get_object_or_404(Composant, id=id)
        OldPrix = Inst.Prix_achat
        form = Composantform(request.POST,instance=Inst)
        if form.is_valid():
            composant = form.save()
            if composant.Prix_achat!=OldPrix:
                UpdatePrixElement(id)
        return redirect('composant')
@csrf_exempt
def composantDelete(request, id=0):
    if(LoginVerfication(request)==-1):return redirect('Login')
    try:
        NembreComposant = Composant.objects.all().count()
        Composantoseuil = Composant.objects.filter(seuil__gt=F('quantite'))
        Inst = get_object_or_404(Composant, id=id)
        if request.method == 'POST':
            Inst.delete()
            return redirect('composant')
        if request.method == 'GET':
            DeletedInst = get_object_or_404(Composant, id=id)
            return  render(request, "composant.html", {"NembreComposant":NembreComposant,"DeletedInst":DeletedInst,"Composantoseuil":Composantoseuil})
    except Composant.DoesNotExist:
        return render(request, 'composant_not_found.html')

def CommandePage(request):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreCommande = Commande.objects.all().count()
        formCommande = Commandeform()
        Commandes = Commande.objects.all()
        for c in Commandes:
            c.resttopaye = c.Prix_commande - c.Prix_Paye
        return  render(request, "Commande.html", {"Commandes":Commandes,"NembreCommande":NembreCommande,"formCommande":formCommande})
    if request.method == 'POST':
        commande = None
        Msg = ""
        form = Commandeform(request.POST)

        if form.is_valid():
            commande = form.save(commit=False)
            deliver = request.POST.get('deliver')
            cuisine_id = request.POST.get('Cuisine')
            if deliver:
                if cuisine_id != "":
                    Inst = get_object_or_404(Cuisine, id=cuisine_id)
                    if Inst.quantite > 0:
                        Inst.quantite -= 1
                        Inst.save()
                    else:
                        commande.deliver = False
                        Msg = "Cuisine Quantité insuffisant"
                else:
                    commande.deliver = False
                    Msg = "Cuisine Non sélectionné"
            commande.save()
        if commande is not None:
            commande = Commande.objects.get(pk=commande.pk)
            if Msg!="":
                return redirect('Commande', id=commande.id , Msg=Msg)
            else :
                return redirect('Commande',id=commande.id)
        return redirect('Commande')
    

def CommandeEdit(request,id=0,Msg=""):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreCommande = Commande.objects.all().count()
        formCommande = Commandeform()
        Inst = get_object_or_404(Commande, id=id)
        selectedCommande = Commandeform(instance=Inst)
        return  render(request, "Commande.html", {"Msg":Msg,"NembreCommande":NembreCommande,"formCommande":formCommande,"selectedCommande":selectedCommande})
    if request.method == 'POST':
        Msg = ""
        commandeInst = get_object_or_404(Commande, id=id)
        commandedeliver = commandeInst.deliver
        form = Commandeform(request.POST,instance=commandeInst)
        if form.is_valid():
            commande = form.save(commit=False)
            deliver = request.POST.get('deliver')
            cuisine_id = request.POST.get('Cuisine')
            if commandedeliver==False:
                print(type(deliver))
                if deliver=="True":
                    if cuisine_id != "":
                        Inst = get_object_or_404(Cuisine, id=cuisine_id)
                        if Inst.quantite > 0:
                            print(Inst.quantite)
                            Inst.quantite -= 1
                            Inst.save()
                        else:
                            commande.deliver = False
                            Msg = "Cuisine Quantité insuffisant"
                    else:
                        commande.deliver = False
                        Msg = "Cuisine Non sélectionné"
            else:
                print(deliver)
                if deliver=="False":
                    print('gg')
                    commande.deliver = True
                    Msg = "déjà livré"
            commande.save()
        if Msg!="":
            return redirect('Commande',id=id, Msg=Msg)
        else :
            return redirect('Commande',id=id)
@csrf_exempt
def CommandeDelete(request, id=0):
    if(LoginVerfication(request)==-1):return redirect('Login')
    try:
        NembreCommande = Commande.objects.all().count()
        Inst = get_object_or_404(Commande, id=id)
        if request.method == 'POST':
            Inst.delete()
            return redirect('Commande')
        if request.method == 'GET':
            DeletedInst = get_object_or_404(Commande, id=id)
            return  render(request, "Commande.html", {"NembreCommande":NembreCommande,"DeletedInst":DeletedInst})
    except Commande.DoesNotExist:
        return render(request, 'Commande_not_found.html')
    
def CuisinePage(request):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreCuisine = Cuisine.objects.all().count()
        formCuisine = Cuisineform()
        Cuisines = Cuisine.objects.all()
        Formelements = Element_cuisineForm()
        return  render(request, "Cuisine.html", {"Cuisines":Cuisines, 'Formelements': Formelements,"NembreCuisine":NembreCuisine,"formCuisine":formCuisine})
    if request.method == 'POST':
        Msg=""
        form = Cuisineform(request.POST)
        cuisine=None
        if form.is_valid():
            cuisine = form.save()
            elements_data = request.POST.getlist('Element')
            quantities = request.POST.getlist('Quantite')
            Element_quantite = request.POST.get('quantite')
            if float(Element_quantite) > 0:
                sufficient_quantity = True  
                for i, element_id in enumerate(elements_data):
                    element = Element.objects.get(pk=element_id)
                    required_quantity = float(quantities[i]) * float(Element_quantite)
                    if element.quantite < required_quantity:
                        sufficient_quantity = False
                        Msg = f"Quantite de {element.Nom} est insuffisant"
                        break  

                if sufficient_quantity:
                    for i, element_id in enumerate(elements_data):
                        element = Element.objects.get(pk=element_id)
                        element.quantite -= float(quantities[i])*float(Element_quantite)
                        element.save()
                else:
                    cuisine.quantite = 0
            for i, element_id in enumerate(elements_data):# calcul Prix achat vente
                element = Element.objects.get(pk=element_id)
                quantity = float(quantities[i])
                element_prix_achat = element.Prix_achat * quantity
                element_prix_vente = element.Prix_vente * quantity

                cuisine.Prix_achat += element_prix_achat
                cuisine.Prix_vente += element_prix_vente

                Element_cuisine.objects.create(Element=element, Cuisin=cuisine, Quantite=quantity)
            cuisine.Prix_achat = extract_three_digits_after_decimal(cuisine.Prix_achat)
            cuisine.Prix_vente = extract_three_digits_after_decimal(cuisine.Prix_vente)
            cuisine.save()
        else :
            print(form.errors)
        if cuisine is not None:
            cuisine = Cuisine.objects.get(pk=cuisine.pk)
            print(Msg)
            if Msg!="":
                return redirect('Cuisine', id=cuisine.id,Msg=Msg)
            else:
                return redirect('Cuisine', id=cuisine.id)
        return redirect('Cuisine')
        
def CuisineEdit(request,id=0,Msg=""):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreCuisine = Cuisine.objects.all().count()
        formCuisine = Cuisineform()
        Inst = get_object_or_404(Cuisine, id=id)
        selectedCuisine = Cuisineform(instance=Inst)
        Formelements = Element_cuisineForm()
        ElementAll = Element_cuisine.objects.filter(Cuisin__id=id)
        Formset = []
        for el in ElementAll:
            form = Element_cuisineForm(instance=el)
            Formset.append(form)
        print(Formset)
        return  render(request, "Cuisine.html", {"Msg":Msg,"Formset":Formset,"Formelements":Formelements, 'selectedCuisine': selectedCuisine,"NembreCuisine":NembreCuisine,"formCuisine":formCuisine})
    if request.method == 'POST':
        Msg=""
        cuisine_instance = get_object_or_404(Cuisine, id=id)
        Element_quantite = float(request.POST.get('quantite'))-cuisine_instance.quantite
        Old_quantite = cuisine_instance.quantite
        form = Cuisineform(request.POST, instance=cuisine_instance)
        if form.is_valid() :
            cuisine = form.save()
            elements_data = request.POST.getlist('Element')
            quantities = request.POST.getlist('Quantite')
            if float(Element_quantite) != 0:
                sufficient_quantity = True  
                if float(Element_quantite) > 0:
                    for i, element_id in enumerate(elements_data):
                        element = Element.objects.get(pk=element_id)
                        required_quantity = float(quantities[i]) * float(Element_quantite)
                        if element.quantite < required_quantity:
                            sufficient_quantity = False
                            Msg = f"Quantite de {element.Nom} est insuffisant"
                            break  
                if sufficient_quantity:
                    for i, element_id in enumerate(elements_data):
                        element = Element.objects.get(pk=element_id)
                        element.quantite -= float(quantities[i])*float(Element_quantite)
                        element.save()
                else:
                    cuisine.quantite = Old_quantite
            NumElementOld = Element_cuisine.objects.filter(Cuisin=cuisine_instance).count()
            if float(request.POST.get('quantite'))==0:
                cuisine.Prix_achat = 0
                cuisine.Prix_vente = 0
                Element_cuisine.objects.filter(Cuisin=cuisine_instance).delete()
                for i, element_id in enumerate(elements_data):
                    element = Element.objects.get(pk=element_id)
                    quantity = float(quantities[i])
                    element_prix_achat = element.Prix_achat * quantity
                    element_prix_vente = element.Prix_vente * quantity

                    cuisine.Prix_achat += element_prix_achat
                    cuisine.Prix_vente += element_prix_vente

                    Element_cuisine.objects.create(Element=element, Cuisin=cuisine, Quantite=quantity)
                cuisine.Prix_achat = extract_three_digits_after_decimal(cuisine.Prix_achat)
                cuisine.Prix_vente = extract_three_digits_after_decimal(cuisine.Prix_vente)
            else :
                if NumElementOld!=len(quantities):
                    Msg = "on peut pas changer les elements de Cuisin deja existant dans le stock" 
            cuisine.save()
        if Msg!="":
            return redirect('Cuisine',id=id,Msg=Msg)
        else:
            return redirect('Cuisine',id=id)
@csrf_exempt
def CuisineDelete(request, id=0):
    if(LoginVerfication(request)==-1):return redirect('Login')
    try:
        NembreCuisine = Cuisine.objects.all().count()
        Inst = get_object_or_404(Cuisine, id=id)
        if request.method == 'POST':
            Inst.delete()
            return redirect('Cuisine')
        if request.method == 'GET':
            DeletedInst = get_object_or_404(Cuisine, id=id)
            return  render(request, "Cuisine.html", {"NembreCuisine":NembreCuisine,"DeletedInst":DeletedInst})
    except Cuisine.DoesNotExist:
        return render(request, 'Cuisine_not_found.html')
    

def ElementPage(request):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreElement = Element.objects.all().count()
        formElement = Elementform()
        Elementseuil = Element.objects.filter(seuil__gt=F('quantite'))
        Elements = Element.objects.all()
        Formelements = Composant_ElementForm()
        return  render(request, "Element.html", {"Elementseuil":Elementseuil,"Elements":Elements, 'Formelements': Formelements,"NembreElement":NembreElement,"formElement":formElement})
    if request.method == 'POST':
        Msg=""
        form = Elementform(request.POST)
        element = None
        if form.is_valid():
            element = form.save()
            comopsants_data = request.POST.getlist('composant')
            if element.type == 'construit':
                quantities = request.POST.getlist('Quantite')
                Langeurs = request.POST.getlist('Langeur')
                Largeurs = request.POST.getlist('Largeur')
                Element_quantite = request.POST.get('quantite')
                if float(Element_quantite) > 0:
                    sufficient_quantity = True  
                    for i, composant_id in enumerate(comopsants_data):
                        composant = Composant.objects.get(pk=composant_id)
                        if Langeurs[i] !='' and Largeurs[i] !='':
                            langeur_i = float(Langeurs[i])
                            largeur_i = float(Largeurs[i])
                            quantity = float((largeur_i * langeur_i  ) / (composant.Largeur * composant.Langeur ) )
                        else:
                            quantity = float(quantities[i])
                        required_quantity = quantity * float(Element_quantite)
                        if composant.quantite < required_quantity:
                            sufficient_quantity = False
                            Msg = f"Quantite de {composant.Nom} est insuffisant"
                            break  
                    if sufficient_quantity:
                        for i, composant_id in enumerate(comopsants_data):
                            composant = Composant.objects.get(pk=composant_id)
                            if Langeurs[i] !='' and Largeurs[i] !='':
                                langeur_i = float(Langeurs[i])
                                largeur_i = float(Largeurs[i])
                                quantity = float((largeur_i * langeur_i  ) / (composant.Largeur * composant.Langeur ) )
                            else:
                                quantity = float(quantities[i])
                            composant.quantite -= quantity*float(Element_quantite)
                            composant.quantite = extract_three_digits_after_decimal(composant.quantite)
                            composant.save()
                    else:
                        element.quantite = 0
                element.Prix_achat = 0
                element.Prix_vente = 0
                for i, composant_id in enumerate(comopsants_data):
                    composant = Composant.objects.get(pk=composant_id)
                    if Langeurs[i] !='' and Largeurs[i] !='':
                        langeur_i = float(Langeurs[i])
                        largeur_i = float(Largeurs[i])
                        quantity = float((largeur_i * langeur_i  ) / (composant.Largeur * composant.Langeur ) )
                    else:
                        quantity = float(quantities[i])

                    element_prix_achat = composant.Prix_achat * quantity

                    element.Prix_achat += element_prix_achat
                    element.Prix_vente += element_prix_achat

                    Composant_Element.objects.create(Element=element, composant=composant, Quantite=extract_three_digits_after_decimal(quantity))
                element.Prix_achat = extract_three_digits_after_decimal(element.Prix_achat)
                element.Prix_vente = extract_three_digits_after_decimal(element.Prix_vente)
                element.save()
        else :
            print(form.errors)
        if element is not None:
            element = Element.objects.get(pk=element.pk)
            if Msg!="":
                return redirect('Element', id=element.id,Msg=Msg)
            else:
                return redirect('Element', id=element.id)
        return redirect('Element')

def ElementEdit(request,id=0,Msg=""):
    if(LoginVerfication(request)==-1):return redirect('Login')
    if request.method == 'GET':
        NembreElement = Element.objects.all().count()
        Elementseuil = Element.objects.filter(seuil__gt=F('quantite'))
        formElement = Elementform()
        Inst = get_object_or_404(Element, id=id)
        selectedElement = Elementform(instance=Inst)
        Formelements = Composant_ElementForm()
        ElementAll = Composant_Element.objects.filter(Element=id)
        Formset = []
        for el in ElementAll:
            form = Composant_ElementForm(instance=el)
            Formset.append(form)
        return  render(request, "Element.html", {"Msg":Msg,"Elementseuil":Elementseuil,"Formset":Formset,"Formelements":Formelements, 'selectedElement': selectedElement,"NembreElement":NembreElement,"formElement":formElement})
    if request.method == 'POST':
        Msg=""
        Element_instance = get_object_or_404(Element, id=id)
        Element_quantite = float(request.POST.get('quantite'))-Element_instance.quantite
        Old_quantite = Element_instance.quantite
        Old_Prix = Element_instance.Prix_achat
        form = Elementform(request.POST, instance=Element_instance)
        if form.is_valid():
            element = form.save()
            # change quantite composant
            if element.type == 'construit':
                comopsants_data = request.POST.getlist('composant')
                quantities = request.POST.getlist('Quantite')
                Langeurs = request.POST.getlist('Langeur')
                Largeurs = request.POST.getlist('Largeur')
                if float(Element_quantite) != 0:
                    sufficient_quantity = True  
                    if float(Element_quantite) > 0:
                        for i, composant_id in enumerate(comopsants_data):
                            composant = Composant.objects.get(pk=composant_id)
                            if Langeurs[i] !='' and Largeurs[i] !='':
                                langeur_i = float(Langeurs[i])
                                largeur_i = float(Largeurs[i])
                                quantity = float((largeur_i * langeur_i  ) / (composant.Largeur * composant.Langeur ) )
                            else:
                                quantity = float(quantities[i])
                            required_quantity = quantity * float(Element_quantite)
                            if composant.quantite < required_quantity:
                                sufficient_quantity = False
                                Msg = f"Quantite de {composant.Nom} est insuffisant"
                                break  
                    if sufficient_quantity:
                        for i, composant_id in enumerate(comopsants_data):
                            composant = Composant.objects.get(pk=composant_id)
                            if Langeurs[i] !='' and Largeurs[i] !='':
                                langeur_i = float(Langeurs[i])
                                largeur_i = float(Largeurs[i])
                                quantity = float((largeur_i * langeur_i  ) / (composant.Largeur * composant.Langeur ) )
                            else:
                                quantity = float(quantities[i])
                            composant.quantite -= quantity*float(Element_quantite)
                            composant.quantite = extract_three_digits_after_decimal(composant.quantite)
                            composant.save()
                    else:
                        element.quantite = Old_quantite
                NumElementOld = Composant_Element.objects.filter(Element=Element_instance).count()
                if float(request.POST.get('quantite'))==0:
                    element.Prix_achat = 0
                    Composant_Element.objects.filter(Element=Element_instance).delete()
                    for i, composant_id in enumerate(comopsants_data):
                        composant = Composant.objects.get(pk=composant_id)
                        if Langeurs[i] !='' and Largeurs[i] !='':
                            langeur_i = float(Langeurs[i])
                            largeur_i = float(Largeurs[i])
                            quantity = float((largeur_i * langeur_i  ) / (composant.Largeur * composant.Langeur ) )
                        else:
                            quantity = float(quantities[i])

                        element_prix_achat = composant.Prix_achat * quantity

                        element.Prix_achat += element_prix_achat

                        Composant_Element.objects.create(Element=element, composant=composant, Quantite=extract_three_digits_after_decimal(quantity))
                    element.Prix_achat = extract_three_digits_after_decimal(element.Prix_achat)
                else :
                    if NumElementOld!=len(quantities):
                        Msg = "on peut pas changer les composant d`element deja existant dans le stock" 
                element.save()
                if element.Prix_achat!=Old_Prix:
                    update_prix_achat_cuisine(element.id)
        else :
            print(form.errors)
        if Msg!="":
            return redirect('Element', id=id,Msg=Msg)
        else:
            return redirect('Element', id=id)
@csrf_exempt
def ElementDelete(request, id=0):
    if(LoginVerfication(request)==-1):return redirect('Login')
    try:
        NembreElement = Element.objects.all().count()
        Inst = get_object_or_404(Element, id=id)
        if request.method == 'POST':
            Inst.delete()
            return redirect('Element')
        if request.method == 'GET':
            DeletedInst = get_object_or_404(Element, id=id)
            return  render(request, "Element.html", {"NembreElement":NembreElement,"DeletedInst":DeletedInst})
    except Element.DoesNotExist:
        return render(request, 'Element_not_found.html')
########################## update Prix
def UpdatePrixElement(composant_id):
    ElementsC = Composant_Element.objects.filter(composant=composant_id)
    Elment_Ids = ElementsC.values_list('Element', flat=True)
    Elements = Element.objects.filter(id__in=Elment_Ids)
    for el in Elements:
        composant_elements = Composant_Element.objects.filter(Element=el)
        prix_achat = 0.0
        for ce in composant_elements:
            prix_achat += ce.composant.Prix_achat * ce.Quantite
        el.Prix_achat = extract_three_digits_after_decimal(prix_achat)
        el.save()
        update_prix_achat_cuisine(el.id)

def update_prix_achat_cuisine(cuisine_id):
    element_cuisines = Element_cuisine.objects.filter(Element=cuisine_id)
    cuisine_ids = element_cuisines.values_list('Cuisin', flat=True)
    cuisines = Cuisine.objects.filter(id__in=cuisine_ids)
    print(cuisine_ids)
    for cuisine in cuisines:
        prix_achat_cuisine = 0.0  
        cuisine_cuisines = Element_cuisine.objects.filter(Cuisin=cuisine)
        for ec in cuisine_cuisines:
            prix_achat_cuisine += ec.Element.Prix_achat * ec.Quantite
        cuisine.Prix_achat = extract_three_digits_after_decimal(prix_achat_cuisine)
        cuisine.save()  
#################################################################### 
def extract_three_digits_after_decimal(number):
    # Multiply the number by 1000 to shift the digits three places to the left.
    shifted_number = number * 1000

    # Use the int() function to convert the float to an integer, effectively truncating the digits after the decimal point.
    truncated_number = int(shifted_number)

    # Extract the last three digits by taking the remainder when divided by 1000.
    three_digits = truncated_number % 1000

    # Extract the third digit (hundreds) and check if it is greater than 5.
    third_digit = (three_digits // 100) % 10
    if third_digit > 5:
        # If the third digit is greater than 5, increment the truncated_number by 1 to round up.
        truncated_number += 1

    # Return the rounded number by dividing it back by 1000.
    return truncated_number / 1000

############# test matplotlib
'''def scatter_plot(request):
    # Your data processing logic here to get x and y data for the plot
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 1, 3, 5]

    plt.scatter(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot')
    
    # Save the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()  # Close the plot to free up memory

    return render(request, 'scatter_plot.html', {'plot_data': plot_data})'''