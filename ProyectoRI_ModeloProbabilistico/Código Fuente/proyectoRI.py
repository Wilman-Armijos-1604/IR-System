# -*- coding: utf-8 -*-
"""ProyectoRI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QYqTTbUeDAT96pqk3Eu_O6ItY5P3kxCS
"""

pip install spacy

!python -m spacy download es_core_news_md

!python -m spacy download en_core_web_md

!python -m spacy download es

import math

"""#Limpieza"""

import spacy
import nltk
from nltk import SnowballStemmer
spanishstemmer=SnowballStemmer('spanish')
import spacy
nlp = spacy.load('es')

def limpiar(text):
  doc = nlp(text)
  tokens = [tok.lemma_.lower() for tok in doc if not tok.is_punct | tok.is_stop | len(tok) < 3]
  stems = [spanishstemmer.stem(token) for token in tokens]
  return stems

def contar_terminos(data):
  result=dict.fromkeys(data,0)
  for item in data:
    if item not in result.keys():
      result[item] = 1
    else:
      result[item] += 1    
  return result

def ponerId(listaDocuemntos):
  id_mas_docuemntos= dict.fromkeys(documentos)
  for i in range(len(documentos)):
    id_mas_docuemntos[documentos[i]]=i+1
  return id_mas_docuemntos

from numpy.lib.function_base import append

def indexarDocuemntos(documentos):
  terminos=[]
  terminos_doc=[]
  terminos_docuementos = dict.fromkeys(documentos)
  for doc in documentos:
    terminos_doc.clear
    with open(doc+".txt", 'r') as file:
      data = file.read().replace('\n', '')
      data_limpia = limpiar(data)
      contar_terminos
      terminos_docuementos[doc]= contar_terminos(data_limpia)
      terminos = terminos + data_limpia
  terminos = list(set(terminos))

  terminos = dict.fromkeys(terminos,[])

  lista=[]
  for item in terminos:
    lista=[]
    for termino_doc in terminos_docuementos:
      if item in terminos_docuementos[termino_doc]:
        lista = lista + [(documentos[termino_doc],terminos_docuementos[termino_doc][item])]
 
    terminos[item]=lista

  return terminos

"""#Modelo"""

def encontrar_ci(documentos, documentosRelevantes):
  terminos=[]
  terminos_documentos = dict.fromkeys(documentos)

  for key , value in documentos.items():
    
    data_limpia = limpiar(value)
    print(data_limpia)
    terminos_documentos[key]= contar_terminos(data_limpia)
    terminos = terminos + data_limpia

  terminos = sorted(list(set(terminos)))

  dict_terminos_ri = dict.fromkeys(terminos, 0)
  dict_terminos_ni_ri = dict.fromkeys(terminos, 0)
  dict_terminos_ci = dict.fromkeys(terminos, 0)
  for key , value in dict_terminos_ri.items():
    for i in range(len(documentos.keys())):
      if (key in terminos_documentos[i+1].keys()) and (i<documentosRelevantes):
        dict_terminos_ri[key] = dict_terminos_ri[key] + 1
      elif (key in terminos_documentos[i+1].keys()) and (i>=documentosRelevantes):
        dict_terminos_ni_ri[key]=dict_terminos_ni_ri[key]+1


  for key  in dict_terminos_ri.keys():
    dict_terminos_ci[key] = math.log10(((dict_terminos_ri[key]+0.5)/(documentosRelevantes-dict_terminos_ri[key]+0.5))/((dict_terminos_ni_ri[key]+0.5)/(len(documentos.keys())-documentosRelevantes-dict_terminos_ni_ri[key]+0.5)))


  return dict_terminos_ci,terminos_documentos

def modelo_probabilistico(ci, documentosLimpios, consulta):
  consulta_arreglo=limpiar(consulta)
  similitud = dict.fromkeys(documentosLimpios,0)

  for key, value in documentosLimpios.items():
    contador = 0
    for item in value.keys():
      if item in consulta_arreglo:
        similitud[key] = similitud[key] + ci[item]
        contador = contador+1
    if contador==0:
      similitud[key]="n/a"
  
  return similitud

def ponerId2(listaDocuemntos):
  ids = range(1,len(listaDocuemntos)+1)
  dict_doc = dict.fromkeys(ids)
  for doc in dict_doc.keys():
    dict_doc[doc] = listaDocuemntos[doc-1]
  return dict_doc

def recuperarDocumentos():
  with open("doc1.txt", 'r') as file:
      d1 = file.read().replace('\n', '')
  with open("doc2.txt", 'r') as file:
      d2 = file.read().replace('\n', '')
  with open("doc3.txt", 'r') as file:
      d3 = file.read().replace('\n', '')
  
  return d1,d2,d3

def consulta_usuario(q1):
  q1 = limpiar(q1)
  q1 = " ".join(q1)
  similitud = modelo_probabilistico(ci,documentosLimpios,q1)
  print("Respuesta de la consulta: ",q1," =")
  for key, value in similitud.items():
    print("Sim(q, d%s)= %s"%(key,value))
  for key, value in similitud.items():
    if (value=="n/a"):
      similitud[key]=0
  lista = list(similitud.values())
  maximo = max(lista)
  for key, value in similitud.items():
    if value == maximo:
      print(f"El mejor documento es {key} con un valor de {value}")

"""#Ejecución de Modelo"""

d1,d2,d3 = recuperarDocumentos()
docs = [d1,d2,d3]
documentos = ponerId2(docs)
ci, documentosLimpios = encontrar_ci(documentos, 1)

print("Ingrese la consulta que desea")
q1 = input()
consulta_usuario(q1)