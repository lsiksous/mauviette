import os.path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import requests
from bs4 import BeautifulSoup
    
from PIL import Image
from io import BytesIO

import re
import json


def save_poster(imdb_id, img_url):
    '''
    Function that fetches and save the poster image from provided url
    and saves it with the provided id (corresponding with IMDb).
    
    INPUT:  id from imdb, url where to find image
    OUTPUT: boolean flag if saved or not.
    '''

    # Get image data, and save it as imdb_id
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    print(f'Saving {imdb_id}')
    img.save(f'data/posters/{imdb_id}.jpg')
    
    return True

# get title of movie
def title(index):
    return df[df.index == index]["movie_title"].values[0]

# get index of movie
def index(movie_title):
    return df[df.movie_title == movie_title]["index"].values[0]

df = pd.read_csv('./data/df_final.csv')
df = df.set_index('id')

imdb_base_url = 'https://www.imdb.com/title/'

#posters = df.loc['tt0756683':].index
posters = df.index

for poster in posters:
    print(f'processing {poster}')
    
    imdb_full_url = imdb_base_url + poster

    # Check to see if I already have it
    if os.path.isfile(f'data/posters/{poster}.jpg'):
        print(f'{poster}: we already have that one !')
    else:
        r = requests.get(imdb_full_url).content
        soup = BeautifulSoup(r, 'html.parser')

        json_dict = json.loads(str(soup.findAll('script',
                                                {'type':'application/ld+json'})[0].text))
        poster_url = json_dict['image']
        save_poster(poster, poster_url)
