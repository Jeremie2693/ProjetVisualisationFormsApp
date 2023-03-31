# ProjetVisualisationFormsApp

Objectif du Projet : 
L’outil est une application web développé en Django. 
L’idée de l’application est de pouvoir générer automatiquement et dynamiquement une page de rapport Html et que l’on puisse ajouter du texte en dessus, et enfin l’exporter en PDF pu en Word. En ayant des données issues de Microsoft Forms,

I/ Fonctionnement générale du code :

L’outil est une application web développé en Django. Le langage de programmation est essentiellement du Python pour la partie backend, Javascript et Html pour la partie frontend. 
L’idée de l’application est de pouvoir générer automatiquement et dynamiquement une page de rapport Html, et que l’on puisse ajouter du texte en dessus, et enfin l’exporter en PDF. 
Le projet peut être découpé en 3 parties :
Première partie concernant l’importation des données, on doit pouvoir importer des données issues de MS Forms. Le choix est fait de ne prendre uniquement les sorties exportées par forms, donc .xlsx. 
Deuxième partie concernant la visualisation des graphiques, on doit générer une page suivant le nombre de colonne du dataset, on aura un graphique. J’ai choisi de réaliser les graphiques avec la libraire Chart.js, qui permet de faire de beaux graphiques sur une page web, en intégrant les données à la page.
On a des boutons de customisation, notamment changer le graphique, ou ajouter un texte. Il faut différentier les questions choix multiple et ouverte. On a une détection automatique du type de question, et suivant cela l’affichage est différent.
Troisième partie concernant l’exportation du rapport, où l’on veut exporter le rapport crée, au format souhaité. 


I/ Comment faire marcher l’application :

En local :
Etape 1 : Ouverture du dossier projet.

Etape 2 : ouverture du terminal du dossier ( clic droit + nouveau terminal du dossier)
 
Etape 3 : (écrire  le script pour lancer le serveur web en local)
 
Etape 5 : aller sur la page :  port d’écoute + /importation/ ici : http://127.0.0.1:8000/importation/
 
Etape 6 : utiliser l’outil : cliquer sur choisir le fichier  
Etape 7 : cliquer sur upload (redirection sur la page Analyse)
Etape 8 : Etape analyse de résultat changement de graphique, ajout de texte.   
  
Etape 9 : cliquer sur Exportation des résultats : choisir le format puis exporter , avec aperçu ou télécharger.
  
 
Après déploiement, il y a juste besoin d’aller sur la page web associer à l’application. Et utiliser l’application comme à l’étape 6.


II/ Fonctionnement plus en détail du code :


Pour des explications détaillé sur le code voir le rapport technique : 





