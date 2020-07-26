import requests
import tweepy
import time
import os
from os import environ

auth = tweepy.OAuthHandler(environ["CONSUMER_TOKEN"], environ["CONSUMER_SECRET"])
auth.set_access_token(environ["KEY"], environ["SECRET"])


tweetMOTD = 'true'
response = requests.get('https://fortnite-api.com/v2/news/br?language=es')
MOTDs = response.json()['data']
api = tweepy.API(auth)

setDelay = 60

while 1:
    status = response.json()['status']
    if status != 200:
        print('fortnite-api.com no está disponible.')
    else:
        print('Buscando cambios...')
        MOTDLoop = response.json()['data']
        print('Guardando GET como MOTDLoop')
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
                            api.update_with_media(i['id']+'.png', i['title']+'\n\n'+i['body'])
                            print('Se ha publicado en Twitter: ' +i['id'])
                            try:
                                time.sleep(3)
                                os.remove(i['id']+'.png')
                                print(i['id']+' se ha eliminado correctamente.')
                                MOTDs = response.json()['data']
                            except:
                                print('Error al eliminar las imágenes 60 segundos después de ser publicadas.')
                        except:
                            print('Ha habido un error al publicar el Tweet. O no.')
            except:
                print('Error al guardar la imagen.')
    else:
        print('No se detectan cambios. Buscando de nuevo en 60 segundos.')

    time.sleep(setDelay)
