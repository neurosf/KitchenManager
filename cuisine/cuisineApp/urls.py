from django.urls import path
from . import views

urlpatterns=[
    path('',views.MainPage,name='main'),
    #composant
    path('Login',views.loginPage,name='Login'),
    path('composant',views.composantPage,name='composant'),
    path('composant/<int:id>',views.composantEdit,name='composant'),
    path('composantD/<int:id>',views.composantDelete,name='composantD'),
    # Commande
    path('Commande',views.CommandePage,name='Commande'),
    path('Commande/<int:id>/<str:Msg>/',views.CommandeEdit,name='Commande'),
    path('Commande/<int:id>',views.CommandeEdit,name='Commande'),
    path('CommandeD/<int:id>',views.CommandeDelete,name='CommandeD'),
    # Cuisine
    path('Cuisine',views.CuisinePage,name='Cuisine'),
    path('Cuisine/<int:id>/<str:Msg>/',views.CuisineEdit,name='Cuisine'),
    path('Cuisine/<int:id>',views.CuisineEdit,name='Cuisine'),
    path('CuisineD/<int:id>',views.CuisineDelete,name='CuisineD'),
    # Element
    path('Element',views.ElementPage,name='Element'),
    path('Element/<int:id>/<str:Msg>/',views.ElementEdit,name='Element'),
    path('Element/<int:id>',views.ElementEdit,name='Element'),
    path('ElementD/<int:id>',views.ElementDelete,name='ElementD'),
    # SignOut
    path('SignOut',views.Logout,name='SignOut'),
    ####
    #path('scatter/', views.scatter_plot, name='scatter_plot'),
]