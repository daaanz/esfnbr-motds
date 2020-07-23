import requests
import tweepy
import time
import os
from os import environ

auth = tweepy.OAuthHandler(environ["CONSUMER_TOKEN"], environ["CONSUMER_SECRET"])
auth.set_access_token(environ["KEY"], environ["SECRET"])


response = requests.get('https://fortnite-api.com/v2/news/br?language=es')
MOTDs = response.json()['data']
status = response.json()['status']
tweetMOTD = 'true'

setDelay = 120

while 1:
    if status != 200:
        print('fortnite-api.com no está disponible.')
    else:
        print('Buscando cambios...')
    response = requests.get('https://fortnite-api.com/v2/news/br?language=es')
    MOTDLoop = response.json()['data']
    if MOTDs == MOTDLoop:
        print('Se han detectado cambios...')
        for i in MOTDLoop['motds']:
            try:
                print('Se ha detectado ' +i['id'])
                url = i['image']
                r = requests.get(url, allow_redirects=True)
                open(i['id']+'.png', 'wb').write(r.content)
                print('Se ha guardado correctamente ' +i['id']+'.png')
                if tweetMOTD == 'true':
                    for i in MOTDLoop['motds']: 
                        try:
                            api = tweepy.API(auth)
                            api.update_with_media(i['id']+'.png', i['title']+'\n\n'+i['body'])
                            print('Se ha publicado en Twitter: ' +i['id'])
                            try:
                                time.sleep(3)
                                os.remove(i['id']+'.png')
                                MOTDs = response.json()['data']
                            except:
                                print('Error al eliminar las imágenes 60 segundos después de ser publicadas.')
                        except:
                            print('Ha habido un error al publicar el Tweet.')
            except:
                print('Error al guardar la imagen.')
    else:
        print('No se detectan cambios.')

    time.sleep(setDelay)
