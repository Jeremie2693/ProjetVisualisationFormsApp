# ProjetVisualisationFormsApp

### Objectif du Projet : 
L’outil est une application web développé en Django. 
L’idée de l’application est de pouvoir générer automatiquement et dynamiquement une page de rapport Html et que l’on puisse ajouter du texte en dessus, et enfin l’exporter en PDF pu en Word. En ayant des données issues de Microsoft Forms,

### I/ Fonctionnement générale du code :

L’outil est une application web développé en Django. Le langage de programmation est essentiellement du Python pour la partie backend, Javascript et Html pour la partie frontend. 

Le projet peut être découpé en 3 parties :
Première partie concernant l’importation des données, on doit pouvoir importer des données issues de MS Forms. Le choix est fait de ne prendre uniquement les sorties exportées par forms, donc .xlsx. 
Deuxième partie concernant la visualisation des graphiques, on doit générer une page suivant le nombre de colonne du dataset, on aura un graphique. J’ai choisi de réaliser les graphiques avec la libraire Chart.js, qui permet de faire de beaux graphiques sur une page web, en intégrant les données à la page.
On a des boutons de customisation, notamment changer le graphique, ou ajouter un texte. Il faut différentier les questions choix multiple et ouverte. On a une détection automatique du type de question, et suivant cela l’affichage est différent.
Troisième partie concernant l’exportation du rapport, où l’on veut exporter le rapport crée, au format souhaité. 


### I/ Comment faire marcher l’application :

- Etape Installation :



En local :
- Etape 1 : Ouverture du dossier projet.

- Etape 2 : ouverture du terminal du dossier ( clic droit + nouveau terminal du dossier)
 
- Etape 3 : (écrire  le script pour lancer le serveur web en local)
 
- Etape 5 : aller sur la page :  port d’écoute + /importation/ ici : http://127.0.0.1:8000/importation/
 
- Etape 6 : utiliser l’outil : cliquer sur choisir le fichier  
- Etape 7 : cliquer sur upload (redirection sur la page Analyse)
- Etape 8 : Etape analyse de résultat changement de graphique, ajout de texte.   
  
- Etape 9 : cliquer sur Exportation des résultats : choisir le format puis exporter , avec aperçu ou télécharger.
  
 
Après déploiement, il y a juste besoin d’aller sur la page web associer à l’application. Et utiliser l’application comme à l’étape 6.


### II/ Fonctionnement plus en détail du code :

Pour des explications détaillé sur le code voir le rapport technique : [rapport technique](https://github.com/Jeremie2693/ProjetVisualisationFormsApp/blob/main/CDC:Rapport/Rapport%20Projet%20Rapport%20Forms.docx)


### III/ Perspectives 

 <strong>Le plus dur a été fait tout ce qui vient après c’est de la déco.</strong>

Les 3 parties les plus dur du projet ont été réaliser, à savoir, l’importation et le pré processing, l’analyse et le rendu en html et enfin l’exportation PDF et Word. 
J’ai réussi à exporter et faire en sorte de générer un pdf dynamique et un word, ce qui a été une tache très dure, mais qui aujourd’hui marche. 

Maintenant on peut passer à la déco et s’amuser avec le code pour rendre jolie l’application en termes de graphisme. Des graphiques plus beaux, des boutons plus beaux…
Aussi le rapport généré peut être amélioré, par une typographique choisit, un filigrane ajouté. 

L'application web présentée ici présente de nombreuses perspectives d'amélioration. En effet, il est toujours possible de perfectionner une application informatique, et plusieurs améliorations pourraient être apportées.
La correction des bugs constitue également une priorité pour améliorer l'application. Un bug surprenant est la superposition des graphiques, qui peut survenir lorsqu'on change l'affichage pour un bar-plot, et qui entraîne un changement de graphique non voulu. Il serait possible de supprimer le graphique de la liste des graphiques lorsqu'on change de type d'affichage pour résoudre ce problème. La version 2 aura ces buggs corrigés, et une version 2 sera uploadé dans quelques mois. 

Par ailleurs, plusieurs nouvelles fonctionnalités pourraient être ajoutées pour améliorer l'application. Il serait notamment intéressant d'intégrer de nouveaux types de graphiques, en plus des pie-charts et des bar-charts. Des options de personnalisation pourraient également être mises en place, comme le choix de la couleur ou du nombre de mots affichés. Un bouton pour supprimer les paragraphes, les questions ou les graphiques qui ne sont pas pertinents serait également utile. Enfin, déployer l'application web pour la rendre plus facilement accessible depuis une URL serait un élément clé pour améliorer l'expérience utilisateur.

En somme, il existe de nombreuses pistes d'amélioration pour cette application web. En optimisant l'expérience utilisateur et en ajoutant de nouvelles fonctionnalités, cette application pourrait répondre encore mieux aux besoins de ses utilisateurs


