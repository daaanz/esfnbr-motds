import requests
import tweepy
import time
import os
from io import BytesIO
from PIL import Image
from os import environ

auth = tweepy.OAuthHandler("wZdsf58Ka2jciAifsd5NDg2y1", "FwbZcX6g9vGbpwLyNejLIHdY9KybOhUdEBHVTvXn6YQpa1MpRY")
auth.set_access_token("1285954782545563649-onwph67OZ10ulwjVO8r7p3CIgSFMnD", "tWeoFkLdvv8qZsYBE4wrooaLpFh331Dalj3AT5S9LtGTY")
api = tweepy.API(auth)

res = requests.get('https://fortnite-api.com/v2/news/br?language=es')
motds = res.json()['data']['motds']

setDelay = 60

def download_img(url, file_name):
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    im.save(title + '.jpg')

for i in motds:
    oldMotds = i['id']

while 1:
    for i in motds:
        motdsID = i['id']
    
    if oldMotds != motdsID:
        print('Cambios detectados...')
        for i in motds:
            title = i['title']
            try:
                print('\n' + 'Se ha detectado ' + i['id'])
                url = i['image']
                file = (title + '.jpg')
                download_img(url, file)
                print('Se ha guardado correctamente ' + i['id'] + '.jpg')
                try:
                    api.update_with_media(i['title'] + '.jpg', '📰 | ' + i['title'] + '\n\n' + i['body'])
                    print('Se ha publicado en Twitter (esfnbr) ' + i['title'])
                except:
                    print('No se ha podido publicar en Twitter.')
            except:
                print('No se ha podido guardar correctamente ' + i['id'])
        print('\n' + 'Buscando nuevos cambios en 60 segundos...')
    else:
        print('No se han encontrado cambios en IDs. Intentando de nuevo en 60 segundos...')

    time.sleep(setDelay)

    
