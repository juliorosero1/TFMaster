from nrclex_es import NRCLex
import pandas as pd

#Devuelve un dataframe con la emocion con mayor intensidad y la puntuacin de esta
def intensidad_palabra (text):
    df= pd.DataFrame()
    intensidad= pd.read_csv("intensidadEmociones.csv")

    palabras=NRCLex(text).affect_dict
    listaPalabras=[]

    for palabra in palabras:
        listaPalabras.append(palabra)

    max=-1
    if 'positivo' in NRCLex(text).raw_emotion_scores:
        if 'negativo' in NRCLex(text).raw_emotion_scores:
            if NRCLex(text).raw_emotion_scores['positivo']>NRCLex(text).raw_emotion_scores['negativo']:
                #print("es positivo")
                for palabra in listaPalabras:
                    if not intensidad[intensidad.spanish== palabra].empty:
                        dfPositivo=intensidad[intensidad.emotion.isin(['anticipation', 'trust','surprise', 'joy'])]
                        dfPositivo=dfPositivo[dfPositivo.spanish==palabra]
                        peso=float(dfPositivo.intensidad.max())
                        if peso>max:
                            max=peso
                            df=dfPositivo[dfPositivo.intensidad==max]


            elif NRCLex(text).raw_emotion_scores['positivo']<NRCLex(text).raw_emotion_scores['negativo']:
                #print("es negativo")
                for palabra in listaPalabras:
                    if not intensidad[intensidad.spanish==palabra].empty:
                        dfNegativo= intensidad[intensidad.emotion.isin(['fear', 'anger', 'disgust','sadness'])]
                        dfNegativo=dfNegativo[dfNegativo.spanish==palabra]
                        peso=float(dfNegativo.intensidad.max())
                        if peso>max:
                            max=peso
                            df=dfNegativo[dfNegativo.intensidad==max]

            else:
                #print("evalua por intensidad")
                for palabra in listaPalabras:

                    if not intensidad[intensidad.spanish == palabra].empty:
                        peso=float(intensidad[intensidad.spanish==palabra].intensidad.max())
                        if peso>max:
                            max=peso
                            df=intensidad[intensidad.spanish==palabra]
                            df=df[df.intensidad==max]


        else:
            #print("es positivo+")
            for palabra in listaPalabras:
                if not intensidad[intensidad.spanish==palabra].empty:
                    dfPositivo=intensidad[intensidad.emotion.isin(['anticipation', 'trust','surprise', 'joy'])]
                    dfPositivo=dfPositivo[dfPositivo.spanish==palabra]
                    peso= float(dfPositivo.intensidad.max())
                    if peso>max:
                        max=peso
                        df=dfPositivo[dfPositivo.intensidad==max]


    elif 'negativo' in NRCLex(text).raw_emotion_scores:
        #print("es negativo")
        for palabra in listaPalabras:
            dfNegativo=intensidad[intensidad.emotion.isin(['fear', 'anger', 'disgust','sadness'])]
            dfNegativo=dfNegativo[dfNegativo.spanish==palabra]
            peso= float(dfNegativo.intensidad.max())
            if peso>max:
                max=peso
                df=dfNegativo[dfNegativo.intensidad==max]
    if df.empty:
        df.intensidad=0

    return df


def palabra(text):
    temp=intensidad_palabra(text)
    palabra=None
    if not temp.empty:
        listaTemp= temp.to_numpy().tolist()
        palabra=listaTemp[0][3]

    return palabra

def puntuacionIntensidad(text):
    temp=intensidad_palabra(text)
    puntuacion=None
    if not temp.empty:
        listaTemp= temp.to_numpy().tolist()
        puntuacion=listaTemp[0][4]

    return puntuacion

def emocion(text):
    temp=intensidad_palabra(text)
    emocion=None
    if not temp.empty:
        listaTemp= temp.to_numpy().tolist()
        emocion=listaTemp[0][1]
        if emocion=='anger': emocion='ira'
        elif emocion=='anticipation': emocion='expectante'
        elif emocion=='disgust' : emocion='repulsion'
        elif emocion=='fear': emocion='miedo'
        elif emocion=='joy': emocion='alegria'
        elif emocion=='sadness' : emocion='tristeza'
        elif emocion=='surprise' : emocion='sorpresa'
        elif emocion=='trust': emocion='confianza'

    return emocion
