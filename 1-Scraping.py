from selenium import webdriver
from tqdm import tqdm #barra carga

import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By


import time
import pandas as pd

import secretsx as sec


#############################################
#######   MENÚ DE INGRESO ###################
#df= pd.DataFrame()

inicio= time.time()
data = []
listaLink =[]
paises=[]

#noticia=""
nom_csv=""
opcion= int(input("1. Noticia1 \n2. Noticia2 \n3. Noticia3\n => "))
if opcion== 1:
    noticia="inseguridad  min_faves:5 lang:es until:2024-03-01 since:2024-02-29 -filter:links -filter:replies" #crisis guayaquil // delincuencia, inseguridad lang:es until:2024-03-01 since:2024-02-29 -filter:links -filter:replies
    nom_csv="noti1.csv"
elif opcion==2:
    noticia="covid ansiedad lang:es until:2021-01-03 since:2020-12-03" #navidad
    nom_csv="noti2.csv"
elif opcion==3:
    noticia= ["covid ansiedad lang:es until:2021-04-25 since:2021-04-23",
              "covid ansiedad lang:es until:2021-05-02 since:2021-04-30",
              "covid ansiedad lang:es until:2021-05-09 since:2021-05-07",
              "covid ansiedad lang:es until:2021-05-16 since:2021-05-14"
             ]
    nom_csv="noti3.csv"
    
#mínimo de 5 likes
#inseguridad  min_faves:5 lang:es until:2024-03-01 since:2024-02-29 -filter:links -filter:replies

#test1
#"delincuencia until:2024-01-01 since:2024-01-31"

###################################################
####### INGRESO DE CREDENCIALES ################
#
def ingreso ( driver ) :
    sleep(2)
    login= driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a/div')
    
    login.click()

    sleep(2)
    input= driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
    input.send_keys(sec.email)

    btn= driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')
    btn.click()

    sleep(2)

    try:
        input= driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        input.send_keys(sec.user)

        btn= driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div')
        btn.click()
    except:
        print("error")

    sleep(1)
    input= driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    input.send_keys(sec.passw)

    btn= driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div')
    btn.click()

    sleep(4)
#



###############################################
######### Busqueda Noticia ##################
###############################################
def busqueda( noticia):
    # Busca un campo de búsqueda
    #search_input = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
    sleep(5)

    search_input = driver.find_element(By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')


    #escribe el tipo de noticia a descargar
    search_input.send_keys(noticia)
    search_input.send_keys(Keys.RETURN)
    


    #ultimos
    if navegador==1:
        # FireFox
        #driver.find_element_by_link_text('Latest').click() #OLD
        driver.find_element(By.LINK_TEXT, 'Latest').click()

    elif navegador==2 or navegador==3:
        #Chromium
        #driver.find_element_by_link_text('Más reciente').click() #OLD
        driver.find_element(By.LINK_TEXT, 'Latest').click()




    # Obtener tweets
    #sleep(6)

    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True
    
    #contador
    contador=0

    while scrolling:
        #page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')#OLD
        page_cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

        for card in page_cards[-15:]:

           # tweet = get_tweet_data(card)
            print("###########################################################################################")
            with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
                
                writer = csv.writer(file)
                #writer.writerow(['user', 'handle', 'fecha', 'tweet', 'emoji', 'comentarios', 'likes'])  # Escribir encabezados
                
                if file.tell() == 0:
                    writer.writerow(['user', 'handle', 'fecha', 'tweet', 'emoji', 'comentarios', 'likes'])
 
                
                
                tweet = get_tweet_data(card, writer)
                for card in page_cards:
                    print("#########################################")
                    print("TOTAL TWEETS CAPTURADOS: ", contador)
                    print("#########################################")

                    get_tweet_data(card, writer)
                    contador= contador+1

#######################################################
                if tweet:
                    tweet_id = ''.join(tweet)
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        data.append(tweet)

        scroll_attempt = 0
        while True:
            # check scroll position
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2) # attempt another scroll
            else:
                last_position = curr_position
                break



##################################################
### Trajeta de TWEET
##################################################
def get_tweet_data(card, csv_writer):
   # time.sleep(10000)

   """Extract data from tweet card and write to CSV"""
   try:
        username = card.find_element(By.XPATH, './/span').text
        print(username)

        handle = card.find_element(By.XPATH, './/span[contains(text(), "@")]').text
        print(handle)

        postdate = card.find_element(By.XPATH, './/time').get_attribute('datetime')
        print(postdate)

        comment = card.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[1]').text
        print(comment)

        retweet_cnt = card.find_element(By.XPATH, './/button[@data-testid="retweet"]').text
        print(retweet_cnt)

        like_cnt = card.find_element(By.XPATH, './/button[@data-testid="like"]').text
        print(like_cnt)

        emoji_tags = card.find_elements(By.XPATH, './/img[contains(@src, "emoji")]')
        emoji_list = []
        for tag in emoji_tags:
            filename = tag.get_attribute('src')
            try:
                emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
            except AttributeError:
                continue
            if emoji:
                emoji_list.append(emoji)
        emojis = ' '.join(emoji_list)
        print(emojis)

        if handle != '':
            tweet = (username, handle, postdate, comment, emojis, retweet_cnt, like_cnt)
            print(tweet)
            
            # Escribir en el archivo CSV
            csv_writer.writerow(tweet)

   except NoSuchElementException as e:
        print(f"Error: {e}")
        return



#####################################################
####### Extraer ubicacion##########################
#####################################################
def extraer_ubicacion(driver2):
    sleep(2)
    pais=''
    if driver2.current_url == "https://twitter.com/i/keyboard_shortcuts":
        driver2.back()
        #continue
    
    else:
        try:
            #lugar= driver.find_element_by_xpath('//span[@data-testid="UserLocation"]').text #OLD
            lugar= driver2.find_element(By.XPATH, '//span[@data-testid="UserLocation"]').text 
            #print(lugar)
            pais=lugar
            #print("ULTIMO")
        except NoSuchElementException:
            pais="NA"
            #print(pais)
    return pais






def buscar():

    if opcion != 3:
        busqueda(noticia)
    else:
        for noti in noticia:
            busqueda(noti)
            #search_input = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]') #OLD
            search_input = driver.find_element(By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')

            search_input.send_keys(Keys.CONTROL, 'a')
            search_input.send_keys(Keys.BACK_SPACE)
            sleep(1)

    driver.close()


###############################################
####### Creación archivo sin ubicacion
##############################################
def creaciónTemp():
   with open(nom_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['user', 'handle', 'fecha', 'tweet', 'emoji', 'comentarios', 'likes'])  # Escribir encabezados

        for d in data:
            writer.writerow(d)

##############################################
####### Extracción de Ubicación ########
##############################################

def ubicacion():
    sleep(2)
    ##Ingresar cada usuario
  # data= pd.read_csv (nom_csv)
    data= pd.read_csv ('tweets.csv')

    print("+++++++++++++++")
    #print(len(handle))
    cont=0
    ini= time.time()
    ubicacion=[]

    #ingreso()

    print("\nBuscando localidad:")

    bucle= tqdm(total= data.handle.count(), position=0, leave=False )#barra de carga
    with open('tweetsUbicacion.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow(list(data.columns) + ['ubicacion'])

        driver2 = webdriver.Chrome()
        driver2.implicitly_wait(1)
        driver2.maximize_window()
        driver2.get('https://x.com/')
        driver2.maximize_window()
        
        time.sleep(2)
        ingreso(driver2)
        
        for id_user in data.handle:
            bucle.set_description("Cargando...".format(id_user))#barra de carga
            bucle.update(1)#barra de carga
            
            '''
            if cont%200==0:
                if navegador==1:
                    # FireFox
                    driver = webdriver.Firefox()
                    driver.implicitly_wait(1)
                    driver.maximize_window()
                elif navegador==2:
                    #Chromium
                    driver2 = webdriver.Chrome()
                    driver2.implicitly_wait(1)
                    driver2.maximize_window()
                elif navegador==3:
                    # Edge
                    options = EdgeOptions()
                    options.use_chromium = True
                    driver = Edge(options=options)
            '''
           
            
            
            #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
           
            
            sleep(2.5)
            #busqueda_user= driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]') #OLD
            busqueda_user= driver2.find_element(By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')


            busqueda_user.send_keys(Keys.CONTROL, 'a')
            busqueda_user.send_keys(Keys.BACK_SPACE)
            sleep(1)
            #print(id_user)
            try:
                busqueda_user.send_keys(id_user)
                sleep(1)
                busqueda_user.send_keys(Keys.DOWN, Keys.DOWN, Keys.RETURN)
                # ubicacion.append(extraer_ubicacion(driver2))
                ubicacion_data = extraer_ubicacion(driver2)

            except:
                print("error")
                ubicacion.append("NA")
                print("error")
            sleep(1.5)

            #print(str(cont))

        
        

                # Escribe encabezados solo si el archivo está vacío
            row = data[data['handle'] == id_user].iloc[0].tolist() + [ubicacion_data]
            writer.writerow(row)
                        

            cont=cont+1
            #if cont%200==0:
            #    driver.close()
        fn=time.time()
        print("!!! Tiempo de ejecución: ", str(fn-ini))

        bucle.close()
        driver2.close()

'''
    #####################################################
    ############ Creacion de archivo con ubicacion
    ######################################################
    data=data.assign(locacion=ubicacion)
    data.to_csv(nom_csv,index = False, header=True, encoding="utf-8")
'''
    #fin= time.time()
    #print("Tiempo de ejecucion: ", fin-inicio)


#################################################################


#########################################################################################
#################### Ingreso a Twitter
############################################

######
navegador=2

if navegador==1:
    # FireFox
    print("Abriendo Firefox...")
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()
elif navegador==2:
    #Chromium
    print("Abriendo Chromium...")
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.maximize_window()


# navigate to login screen
#driver.get('https://twitter.com/i/flow/login')
driver.get('https://x.com/')
driver.maximize_window()

#######################################################################################################
## +++++++++++ EJECUCIÓN DEL ALGORITMO +++++++++++++

ingreso(driver)
#buscar()
#creaciónTemp()

#driver.close()
ubicacion()