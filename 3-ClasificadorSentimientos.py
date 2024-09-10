import pandas as pd
from nrclex_es import NRCLex
from textblob import TextBlob
import time
from tqdm import tqdm #barra carga
import IntensidadPalabra_3 as inpa

#import nltk
#nltk.download('punkt_tab')


sentimiento=[]
polaridad=[]

#Agreaga cantidad de palabras de denotasn las expresiones
miedo=[]; ira=[]; expectante=[]; confianza=[]; sorpresa=[]; tristeza=[]; repulsion=[]; alegria=[]; positivo=[]; negativo=[]

#Agrega intensidad palabras
palabra=[]; puntuacionEmocion=[]; emocion=[]

tweetSentimiento =pd.DataFrame()

data = pd.read_csv ('limpiezaXlocacion_2.csv')

tweetSentimiento=tweetSentimiento.assign(id=data.id)
tweetSentimiento=tweetSentimiento.assign(user=data.user)
tweetSentimiento=tweetSentimiento.assign(fecha=data.fecha)
tweetSentimiento=tweetSentimiento.assign(tweet=data.tweet)
#tweetSentimiento=tweetSentimiento.assign(noticia=data.noticia)
tweetSentimiento=tweetSentimiento.assign(pais=data.pais)

tweets= data.tweet

###############################################
#########Asignación de sentimientos############
###############################################
#Inicio de barra de carga
print("\nAnalizando Sentimientos:")
bucle= tqdm(total= data.id.count(), position=0, leave=False )#barra de carga

for tweet in tweets:
    bucle.set_description("Cargando...".format(tweet))#barra de carga
    bucle.update(1)#barra de carga

    #if 'fear' in NRCLex(tweet).raw_emotion_scores: miedo.append(NRCLex(tweet).raw_emotion_scores['fear'])
    if 'miedo' in NRCLex(tweet).raw_emotion_scores: miedo.append(NRCLex(tweet).raw_emotion_scores['miedo'])
    else: miedo.append(0)

    #if 'anger' in NRCLex(tweet).raw_emotion_scores: ira.append(NRCLex(tweet).raw_emotion_scores['anger'])
    if 'ira' in NRCLex(tweet).raw_emotion_scores: ira.append(NRCLex(tweet).raw_emotion_scores['ira'])
    else: ira.append(0)

    #if 'anticipation' in NRCLex(tweet).raw_emotion_scores: expectante.append(NRCLex(tweet).raw_emotion_scores['anticipation'])
    if 'expectante' in NRCLex(tweet).raw_emotion_scores: expectante.append(NRCLex(tweet).raw_emotion_scores['expectante'])
    else: expectante.append(0)

    #if 'trust' in NRCLex(tweet).raw_emotion_scores: confianza.append(NRCLex(tweet).raw_emotion_scores['trust'])
    if 'confianza' in NRCLex(tweet).raw_emotion_scores: confianza.append(NRCLex(tweet).raw_emotion_scores['confianza'])
    else: confianza.append(0)

    #if 'surprise' in NRCLex(tweet).raw_emotion_scores: sorpresa.append(NRCLex(tweet).raw_emotion_scores['surprise'])
    if 'sorpresa' in NRCLex(tweet).raw_emotion_scores: sorpresa.append(NRCLex(tweet).raw_emotion_scores['sorpresa'])
    else: sorpresa.append(0)

    #if 'sadness' in NRCLex(tweet).raw_emotion_scores: tristeza.append(NRCLex(tweet).raw_emotion_scores['sadness'])
    if 'tristeza' in NRCLex(tweet).raw_emotion_scores: tristeza.append(NRCLex(tweet).raw_emotion_scores['tristeza'])
    else: tristeza.append(0)

    if 'repulsion' in NRCLex(tweet).raw_emotion_scores: repulsion.append(NRCLex(tweet).raw_emotion_scores['repulsion'])
    else: repulsion.append(0)

    #if 'joy' in NRCLex(tweet).raw_emotion_scores: alegria.append(NRCLex(tweet).raw_emotion_scores['joy'])
    if 'alegria' in NRCLex(tweet).raw_emotion_scores: alegria.append(NRCLex(tweet).raw_emotion_scores['alegria'])
    else: alegria.append(0)

    #if 'depresion' in NRCLex(tweet).raw_emotion_scores: alegria.append(NRCLex(tweet).raw_emotion_scores['depresion'])
    #if 'depresion' in NRCLex(tweet).raw_emotion_scores: depresion.append(NRCLex(tweet).raw_emotion_scores['depresion'])
    #else: depresion.append(0)


    #if 'positive' in NRCLex(tweet).raw_emotion_scores: positivo.append(NRCLex(tweet).raw_emotion_scores['positive'])
    if 'positivo' in NRCLex(tweet).raw_emotion_scores: positivo.append(NRCLex(tweet).raw_emotion_scores['positivo'])
    else: positivo.append(0)

    #if 'negative' in NRCLex(tweet).raw_emotion_scores: negativo.append(NRCLex(tweet).raw_emotion_scores['negative'])
    if 'negativo' in NRCLex(tweet).raw_emotion_scores: negativo.append(NRCLex(tweet).raw_emotion_scores['negativo'])
    else: negativo.append(0)


bucle.close()
print("Análisis de sentimientos Exitoso")
#Creación de dataframe con los sentimientos de cada oración
tweetSentimiento=tweetSentimiento.assign(miedo=miedo)
tweetSentimiento=tweetSentimiento.assign(ira=ira)
tweetSentimiento=tweetSentimiento.assign(expectante=expectante)
tweetSentimiento=tweetSentimiento.assign(confianza=confianza)
tweetSentimiento=tweetSentimiento.assign(sorpresa=sorpresa)
tweetSentimiento=tweetSentimiento.assign(tristeza=tristeza)
tweetSentimiento=tweetSentimiento.assign(repulsion=repulsion)
tweetSentimiento=tweetSentimiento.assign(alegria=alegria)
#tweetSentimiento=tweetSentimiento.assign(depresion=depresion)
tweetSentimiento=tweetSentimiento.assign(positivo=positivo)
tweetSentimiento=tweetSentimiento.assign(negativo=negativo)

############################################################################
##Creación de dataframe únicamente con la puntuación de los sentimientos#
############################################################################
puntuacion=tweetSentimiento.loc[:,['miedo', 'ira', 'expectante','confianza', 'sorpresa', 'tristeza', 'repulsion', 'alegria']]
listaPuntuacion=puntuacion.to_numpy().tolist()


for marca in listaPuntuacion:
    indice=0
    sent=[]
    if max(marca)!=0:
        for p in marca:
            if max(marca)== p:
                sent.append(puntuacion.columns.values[indice])
            indice= indice+1

    else:  sent.append("NA")

    sentimiento.append(sent)


###########################################################
############################################################
##Creación de dataframe con la polaridad del sentimiento##
#############################################################
posNeg= tweetSentimiento.loc[:,['positivo','negativo']]
listaPosNeg= posNeg.to_numpy().tolist()

print("********************************")
print(tweetSentimiento.loc[:,['positivo','negativo']])
print("********************************")

for marca in listaPosNeg:
    if marca[0]>marca[1]: polaridad.append('positivo')
    elif marca[0]<marca[1]: polaridad.append('negativo')
    elif marca[0]==0 and marca[1]==0: polaridad.append(None)
    else: polaridad.append('neutro')
################################################################

tweetSentimiento=tweetSentimiento.assign(emociones=sentimiento)
tweetSentimiento=tweetSentimiento.assign(polaridad=polaridad)

#################################################################
############### Agrega intensidad de palabras####################
print("\nAnalizando Intensidad de palabras:")
bucle= tqdm(total= tweetSentimiento.id.count(), position=0, leave=False )#barra de carga

for tweet in tweetSentimiento.tweet:
    bucle.set_description("Cargando...".format(tweet))#barra de carga
    bucle.update(1)#barra de carga

    palabra.append(inpa.palabra(tweet))
    emocion.append(inpa.emocion(tweet))
    puntuacionEmocion.append(inpa.puntuacionIntensidad(tweet))

bucle.close()

tweetSentimiento=tweetSentimiento.assign(palabra=palabra)
tweetSentimiento=tweetSentimiento.assign(emocion=emocion)
tweetSentimiento=tweetSentimiento.assign(puntuacion=puntuacionEmocion)
################################################################



###################################################################
###########Opción de  dataframe ###################################

#opcion=input("1. Crear archivo con latitud y longitud\n2. Sin latitud ni longitud:\n => ")
opcion=2 ############ TESTEO############
if opcion== '1':
    ###########Asignación de latitud y longitud#######################
    tweetSentimiento=tweetSentimiento.assign(lon= data.longitud)
    tweetSentimiento=tweetSentimiento.assign(lat= data.latitud)
    tweetSentimiento=tweetSentimiento.dropna(subset=['lat'])


#opcion=input("Desea eliminar valores nulos en el campo Pais? (S/N): => ")
opcion='s' ########TESTEO##############
if opcion =='s' or opcion=='S':
    tweetSentimiento=tweetSentimiento.dropna(subset=['polaridad'])
    tweetSentimiento=tweetSentimiento.dropna(subset=['pais'])
    tweetSentimiento=tweetSentimiento.dropna()

tweetSentimiento.to_csv("sentimientosTweet_3.csv",index = False, header=True, encoding="utf-8")
###########################################################################
print(tweetSentimiento)
print("\n    => Reducción de registros de "+ str(data.id.count())+ " a " + str(tweetSentimiento.id.count())+"\n")
