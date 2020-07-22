import requests
import tweepy
import time
import os
from os import environ

auth = tweepy.OAuthHandler("8IxuETmKvSI5EAUjCPTEGqIhd", "BF94gZ1HLC8uqXNi2mIEmmHbxDOsRv3ISvVGPCS5R2SAnjSLKw")
auth.set_access_token("796105823013441536-5VbjDD4liALPaFicM2gDnx1zCyw2LZY", "L3FPNUjSznOzEQO2slFPa7r2TJkyJvyTTNzDdwjuA4iVH")


response = requests.get('https://fortnite-api.com/v2/news/br?language=es')
MOTDs = response.json()['data']
status = response.json()['status']

setDelay = 120

while 1:
    if status != 200:
        print('fortnite-api.com no está disponible.')
    else:
        print('Buscando cambios...')
    response = requests.get('https://fortnite-api.com/v2/news/br?language=es')
    MOTDLoop = response.json()['data']
    if MOTDs != MOTDLoop:
        print('Se han detectado cambios...')
        for i in MOTDLoop['motds']:
            try:
                print('Se ha detectado ' +i['id'])
                url = i['image']
                r = requests.get(url, allow_redirects=True)
                open(i['id']+'.png', 'wb').write(r.content)
                print('Se ha guardado correctamente ' +['id']+'.png')
                try:
                    api = tweepy.API(auth)
                    api.update_with_media(i['id']+'.png', 'MOTD:\n\n'+i['title']+'\n'+i['body'])
                    print('Se ha publicado en Twitter: ' +i['id'])
                except:
                    print('Ha habido un error al publicar el Tweet.')
            except:
                print('Error al guardar la imagen.')
    else:
        print('No se detectan cambios.')
    time.sleep(setDelay)

