++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

PROJET 2 : Utilisez les bases de Python pour l'analyse de marché

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Installation

1 - Installation de Python3, l'outil d'environnement virtuel et le gestionnaire de paquets (sur Linux UBUNTU)
    
    $ sudo apt-get install python3 python3-venv python3-pip


2 - Mise en place de l'environnement virtuel "env"

    1 - Accès au répertoire du projet :
            
            exemple cd /git/Projet2

    2 - Création de l'environnement virtuel :
            
            $ python3 -m venv env

3 - Ouverture de l'environnement virtuel et ajout des modules

            $ source env/bin/activate
            
            (env) $ pip install -r requirements.txt
            

Utilisation du programme

    1 - Lancement

            $ python3 Script_Projet2.py
    
    2 - Choix

            Choisir 1 pour récuperer les informations et image d'un article dans le repertoire ../Articles et ../Articles/Images 
                
                Veillez à bien copier le nom de l'article exact sur le site

            Choisir 2 pour récupérer les informations d'une catégorie et les images des articles de la catégorie dans le répertoire ../Catégories et ../Catégorie/Images 

                Veillez à bien copier le nom de la catégorie exacte sur le site
        
            Choisir 3 pour récupérer l'ensemble des catégories et images du site dans le répertoire ../Toutes_Categories et ../Toutes_Categories/Images 


