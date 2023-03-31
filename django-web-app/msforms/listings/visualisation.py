import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
from nltk.corpus import stopwords
from wordcloud import WordCloud
import os

# Importation du fichier suivant un chemin
def importation_dataset(file_directory):
    my_file = pd.read_excel(file_directory,index_col=0)
    dataset = pd.DataFrame(data=my_file, index=None)
    return dataset

#pour prendre les métadonnées les données ajouté après exportationds des résultats forms
def metadata(questions):
    if 'Total points' in questions:
        meta_data=questions[:questions.index('Total points')]
    elif 'Nom' in questions:
        meta_data=questions[:questions.index('Nom')+1]
    else: 
        meta_data=[]
    return meta_data

#Fonction pour filtrer les questions
def filter_question(dataset):
    list_question=list(dataset.columns)
    meta_data=metadata(list_question)
    questions=[]
    for q in list_question:
        if len(re.findall(r"^Points|^Feedback",q))>0:
            continue 
        else:
            if q not in meta_data:
                questions.append(q)
    if 'Total points'in questions:
        questions.remove('Total points')
    if 'Quiz feedback'in questions:
        questions.remove('Quiz feedback')
    return questions

# Fonction pour nettoyer les questions
def question_cleanning(list_question):
    questions=[]
    for q in list_question:
        q=q.replace("\n",' ').replace("\xa0",' ')
        questions.append(q)
    return questions

#Fonction pour renomer les colonnes, plus simplement
def name_columns(questions):    
    meta_data=metadata(questions)
    list_questions=[w for w in questions if w not in meta_data]
    col=meta_data
    i=1
    for index in range(1,len(list_questions)+1):
        col.append("Q"+ str(index))   
    return col 
# Fonction pour associer une question raccourcie avec sa question originale
def questions_list(questions):
    new_col_names=name_columns(questions)
    return list(zip(new_col_names,questions))


# Fonction pour nettoyer le dataset
def clean_dataset(dataset):
    dataset.fillna('',inplace=True)
    questions=list(dataset.columns)
    meta_data=metadata(questions)

    questions=filter_question(dataset)

    dataset_cleaned=pd.merge(dataset[meta_data],dataset[questions], left_index = True, right_index = True)
    dataset_cleaned.columns=meta_data+question_cleanning(questions)

    #dataset_cleaned.columns=name_columns(questions)
    #dict_question_columns=dict_questions(questions)
    #return dataset_cleaned,dict_question_columns

    return dataset_cleaned
#filtrer les questions
def questions_dataset(dataset):
    questions=filter_question(dataset)
    return dataset[questions]

#fonction pour avoir le temps moyen des questions
def mean_response_time(dataset_cleaned):
    dataset_cleaned["Horodateur"]=dataset_cleaned["Heure de fin"].dt.date
    dataset_cleaned['Durée de rédaction'] = (dataset_cleaned['Heure de fin'] - dataset_cleaned['Heure de début']).dt.total_seconds() / 60
    
    temps_moyen = round(dataset_cleaned['Durée de rédaction'].mean(),3)

    dataset_cleaned.drop(columns=["Horodateur","Durée de rédaction"], inplace=True)

    return temps_moyen
#enlever les questions choix multiple
def remove_not_multichoice(dataset,liste):
    list_copy=[]
    for elt in dataset[liste].columns:
        if dataset[elt].nunique()>10:
            continue
        else:
            list_copy.append(elt)
    return list_copy
#garder les questions ouverte
def keep_is_verbal(dataset,liste):
    list_multichoice=remove_not_multichoice(dataset,liste)
    return [w for w in liste if w not in list_multichoice]


def bool_list_verbal(dataset):
    bool_list=[]
    for elt in list(dataset.columns):
        if elt in keep_is_verbal(dataset,list(dataset.columns)):
            bool_list.append(True)
        else:
            bool_list.append(False)
    
    return bool_list

#fonction pour netoyer
def clean(s):
    #nettoyage de la chaine du verbatim en enlevant les caractères spéciaux
        
    specialChars = "!?&#$%^*~;@().[]{}'\""
    specialChars="|\\".join(list(specialChars))
    s=re.sub(specialChars," ",s)
    
    s=re.sub(r"\r|\n"," ",s)
    s=re.sub(r"\s+\s+"," ",s)
    

    transTable=s.maketrans("àâäéèêëîïôöùûüÿç", "aaaeeeeiioouuuyc")
    s=s.translate(transTable)
    s=" ".join([word.lower() for word in s.split(" ") ])

    return s

def normalize_text(s,langue='french'):
    
    # normaliser au singulier 
    list_word =s.split()

    # Enlever les stop words
    
    stop_words = stopwords.words(langue) 
    
    
    list_word = [word for word in list_word if word not in stop_words]

    
    normal_list=[word for word in list_word if len(word)>=1]
    
    normal_sentence=" ".join(normal_list)
    
    return normal_sentence

#pour nettoyer le texte
def preprocessing(list_sentence):
    list_sentence=list(map(lambda x: normalize_text(clean(x)),list_sentence))

    try :
        int(list_sentence[len(list_sentence)//2]) 
        list_sentence=[phrase for phrase in list_sentence ]

    except:
        list_sentence=[phrase for phrase in list_sentence if len(phrase)>3]
    return list_sentence



#fonction pour générer les nuages de mots
def plot_cloud(list_sentence,param,max = 1000,color="white", title_size=16):
    
    list_sentence=preprocessing(list_sentence)
    cloud_generator = WordCloud(background_color=color,
                                random_state=1, collocations=False)
    plt.figure(figsize=(20, 10))

    try :
        int(list_sentence[len(list_sentence)//2]) 
        wordscloud=cloud_generator.generate_from_frequencies(dict(Counter(list_sentence)))


    except:
        wordscloud = WordCloud(max_words=max,background_color=color).generate(' '.join(list_sentence)) 
    plt.imshow(wordscloud, interpolation="bilinear")
    plt.title(f"Nuage de mots  ",fontsize = 18,fontweight ='bold')
    plt.axis("off")
    # exporter l'image
    filename = f"wordcloud-{param}.jpeg"
    filepath = "listings/static/listings/images/{}".format(filename)

    plt.savefig(filepath,bbox_inches="tight")