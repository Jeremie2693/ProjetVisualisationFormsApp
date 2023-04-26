#importation librairie
import io
import os
import shutil
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import matplotlib.pyplot as plt
import pandas as pd
from listings.visualisation import *
from django.shortcuts import render
from django.template.loader import get_template
from django.views import View
from django.db import models
from django.apps import apps
from django.db import connection
from collections import Counter
from django.template.loader import render_to_string

#definition de la vue importation
def importation(request):
    global file_directory
    global name

    # Supprimer tous les fichiers d'un dossier
    def delete_files(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Chemin des dossiers où les fichiers seront téléchargés
    media_directory = './listings/static/listings/media/'
    images_directory = './listings/static/listings/images/'

    if request.method == 'POST':
        upload_file = request.FILES["document"]
        print(upload_file)

        # Vérifier si le fichier est en format Excel
        if upload_file.name.endswith('.xlsx'):
            # Supprimer tous les fichiers des dossiers avant d'importer le nouveau fichier
            delete_files(media_directory)
            delete_files(images_directory)

            # Enregistrer le fichier
            savefile = FileSystemStorage()
            name = savefile.save(upload_file.name, upload_file)
            print(name)

            # Enregistrer le chemin du fichier
            file_directory = media_directory + name
            print(file_directory)

            # Lire le fichier
            readfile(file_directory)

            #améliorer le nom
            name=name.split('(')[0]

            # Rediriger vers la vue analyse
            return redirect('analyse')

        else:
            # Afficher un message d'erreur si le fichier n'est pas en format Excel
            messages.warning(request, 'Le fichier n\'a pas été téléchargé, utiliser une extension .xlsx ! c\'est à dire classeur Excel et non fichier csv')

    return render(request, './importation.html')

#la fonction lecture du fichier (en xlsx)
def readfile(filename):

    #global data,my_file,rows
    my_file = pd.read_excel(filename,index_col=0)
    #on transforme en dataframe
    data = pd.DataFrame(data=my_file, index=None)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])


    null_data = data[data.isnull().any(axis=1)]
    missing_values = len(null_data)

# recréation du contexte des données
def context_creation(file_directory):
    
    # Gérer l'exception la personne clique sur le haut alors qu'il n'a pas téléverser de fichier
    if 'file_directory' in globals():

        dataset=importation_dataset(file_directory)
        dataset_cleaned=clean_dataset(dataset)
        dataset_questions=questions_dataset(dataset)
        
        # Données 
        column_names=list(dataset_questions.columns)
        rows=len(dataset_questions)
        avg_time=mean_response_time(dataset_cleaned)

        dashboard = {}
        for col in column_names:
            column_dashboard=[]
            for x in dataset_questions[col]:
                column_dashboard.append(x)

                my_dashboard = dict(Counter(column_dashboard)) 

                sorted_dashboard = sorted(my_dashboard.items(), key=lambda x: x[1], reverse=True)

                listkeys = []
                listvalues = []

                for x in sorted_dashboard:
                    listkeys.append(x[0])
                    listvalues.append(x[1])

                #print(listkeys)
                #print(listvalues)

            dashboard[col]=(listkeys,listvalues)
        #print(dashboard)
        
        #print(dashboard.values())

        listkeys=[key for key,value in dashboard.values()]
        listvalues=[value for key,value in dashboard.values()]

        list_zip_columns=questions_list(column_names)

        list_bool_open_question=bool_list_verbal(dataset_questions)
        
        print(list_bool_open_question)

        boucle_value=list(map(lambda x:(x[0],x[1][0],x[1][1]), list(enumerate(list(zip(column_names,list_bool_open_question))))))
        for col_number,col_name,bool_open in boucle_value:
            if bool_open:
                plot_cloud(listkeys[col_number],col_number)

        #print(list(map(lambda x:(x[0],x[0]+1,x[1],x[2]), boucle_value)))
        context={'list_zip_columns': list(map(lambda x:(x[0],x[0]+1,x[1],x[2]), boucle_value)),
                 'rows':rows,
                 'avg_time':avg_time,
                'listkeys': listkeys,
                'listvalues': listvalues,
                'list_bool_open_question':list_bool_open_question,
                'name_file':name
                  }
        return context

#la vue du fichier
def analyse(request):
    
    if 'file_directory' in globals():
        context=context_creation(file_directory)

        return render(request,'listings/analyse.html', context)

    #if file_directory is None:
    #    messages.warning(request, 'Aucun fichier n\'a pas été téléchargé, veuillez vous rendre sur la page Importation des données pour importer un fichier !')
    #message d'erreur s'il n'y a pas de fichier upload
    else:
        messages.warning(request, 'Aucun fichier n\'a pas été téléchargé, veuillez vous rendre sur la page Importation des données pour importer un fichier !')
        #return redirect('not-upload')
        return render(request,'listings/analyse.html')


#vue d'exportation
def exportation(request):

    return render(request, 'listings/exportation.html')


## partie génération du pdf
from django.http import HttpResponse
from django.views.generic import View

from listings.utils import render_to_pdf 
import docx

import json
from django.conf import settings
from django.http import FileResponse
from docx import Document
from pdf2docx import Converter


#Affichage en pdf : apercu + téléchargement
data = {}
export_format='pdf'
def not_upload(request):
    global data
    global export_format
    template=get_template('listings/pdf.html')
    # Récupérer le chemin absolu du dossier "images"
    image_path = os.path.join(settings.BASE_DIR, './listings/static/listings/images')
    absolute_path = os.path.abspath(image_path)

    if request.method == 'POST':

        if 'file_directory' in globals():

            if os.path.exists(absolute_path):
            # Créer le contexte avec les données du formulaire
                data = context_creation(file_directory)

                # Ajouter le chemin absolu du dossier "media" au contexte
                data['absolute_path'] = absolute_path

                data_request = json.loads(request.body)

                graph_urls = data_request.get('graphUrls')
                export_format = data_request.get('exportFormat')
                textes_commentaires =data_request.get('textes_commentaires')

                #transformer en liste
                graph_urls=list(graph_urls)
                graph_urls=[url.replace("\"","") for url in graph_urls]
                #print(graph_urls)
                textes_commentaires=list(eval(textes_commentaires))

                graph_url_name_list = []
                for i,elt in enumerate(graph_urls):
                    name="graph_url_" + str(i)
                    data[name] = elt
                    graph_url_name_list.append(name)
                #ajout des graphes urls
                data['list_zip_columns'] = list(map(lambda x:(x[0][0],x[0][1],x[0][2],x[0][3],x[1]),list(zip(data['list_zip_columns'],graph_urls))))
                #ajout des graphes commentaires
                data['list_zip_columns']  = [(elem[0][0], elem[0][1], elem[0][2], elem[0][3], elem[1],elem[0][4]) for i, elem in enumerate(list(zip(data['list_zip_columns'],textes_commentaires)))]
        else:
            data = {}
            
        #print(data)
        #html=template.render(data)

        #transformation en pdf
        pdf = render_to_pdf('listings/pdf.html', data)
        #return HttpResponse(html)
        #return render(request, 'listings/pdf.html')
        #dijonction a percu téléchargement

    elif request.method == 'GET':
        print(data)
        #exportation en pdf

        pdf = render_to_pdf('listings/pdf.html', data)

        if export_format == 'pdf':

            if pdf: 
                    
                    response = HttpResponse(pdf, content_type='application/pdf') 
                    #on nomme le fichier
                    filename = "Analyse_resultat_forms.pdf" 
                    content = "inline; filename=%s" %(filename) 
                    download = request.GET.get("download") 
                    #si on appuie le bouton on télécharge
                    if download: 
                        content = "attachment; filename=%s" %(filename) 
                    response['Content-Disposition'] = content 
                    return response
        
        elif export_format == 'word':
            # Generate PDF first
            pdf = render_to_pdf('listings/pdf.html', data)
            filename_pdf = "Analyse_resultat_forms.pdf" 
            content_pdf = "inline; filename=%s" %(filename_pdf) 
            response_pdf = HttpResponse(pdf, content_type='application/pdf') 
            response_pdf['Content-Disposition'] = content_pdf

            # Save PDF to media directory
            media_directory = './listings/static/listings/media/'
            filepath_pdf = os.path.join(media_directory, filename_pdf)
            with open(filepath_pdf, 'wb') as pdf_file:
                pdf_file.write(pdf.content)
                
            download = request.GET.get("download") 
            if download: 
                #content = "attachment; filename=%s" %(filename) 
                #response['Content-Disposition'] = content 
                # Convert PDF to Word
                filename_docx = "Analyse_resultat_forms.docx"
                filepath_docx = os.path.join(media_directory, filename_docx)
                cv = Converter(filepath_pdf)
                cv.convert(filepath_docx)
                cv.close()
                # Return the Word file as a response for download
                with open(filepath_docx, 'rb') as docx_file:
                    response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    content = "attachment; filename=%s" %(filename_docx) 
                response['Content-Disposition'] = content
                return response

        return response_pdf


    return HttpResponse("404 not found")
    



def pdf_view(request):
    return render(request, 'listings/pdf.html')
