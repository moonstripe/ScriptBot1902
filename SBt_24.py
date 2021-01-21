import urllib.request
import time
import facebook
import csv
import textwrap
from PIL import Image, ImageDraw, ImageFont
import random
import os
import requests
import io
import urllib3
import datascience
import numpy as np
import re
from bs4 import BeautifulSoup

##DIALOGUE GEN##
def dialogue_gen (corpus, num):
    story = open(corpus, encoding='utf8').read()
    dialogue = story.split()

    d_markov = secondOrderMarkov(dialogue, num)
    dialogue = d_markov.rsplit('.',1)[0]+"."
    return dialogue

##MARKOV##
def secondOrderMarkov(corpus,words):
    def make_pairs(corpus):
        for i in range(len(corpus)-1):
            yield (corpus[i], corpus[i+1])
    
    pairs = make_pairs(corpus)
    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
            
       
    first_word=random.choice(corpus)
    
    while first_word.islower():
        first_word = np.random.choice(corpus)
    
    chain = [first_word]
    n_words = words
   

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))
    
    return ' '.join(chain)

def post_to_fb(txt, img):
    access_token='EAACVS6jUj0QBAJZCSXTsVSminS2ogpxFKrPvV6HqZBErPtM71jU01riPKb9jFJyvkaZA6phVKZBUXhkZCZCZCFHkKTz4dEUZBRwYo0yNaZCgatG48cMCYnoH1AemUlLo8hgSqTjwzrodV1J67qSUD4FjvEXQUxayfSx7Da74UQFfE8BnZBR000Lucs7WbCdf6Dl5sZD'
    graph = facebook.GraphAPI(access_token, version="3.0")

    post_id = graph.put_photo(image=open(img, 'rb'), message=txt)


    return print("The post "+post_id["id"]+" went live on "+time.ctime(time.time())+".")


def script_runner():

    ##LOCATION##
    with open('SB1902/final_cities.txt') as a:
        f_c = list(a)

    for i in np.arange(len(f_c)):
        f_c[i] = f_c[i][:-1]

    prefix = ['INT.', 'EXT.', 'INT/EXT.']
    rand_city = random.choice(f_c)
    locale = ['HOUSE', 'KITCHEN', 'ALLEY', 'THEATRE', 'BAR', 'BEDROOM', 'FIELD', 'FOREST']
    TOD = ['EARLIER', 'LATER', 'TOMORROW', 'EVENING', 'DAWN', 'DUSK', 'MIDDLE OF NIGHT']
    location = random.choice(prefix)+" "+random.choice(f_c)+" "+random.choice(locale)+" - "+random.choice(TOD)

    ##Characters##
    with open('SB1902/names.csv', newline='') as csvfile:
        scotland = csv.reader(csvfile, delimiter=' ', quotechar='|')
        names = []
        for row in scotland:
            name = row[0]
            names.append(name)

    characters = random.sample(names, 2)
    character1 = characters[0]
    character2 = characters[1]

    ##DESC##
    story = open('SB1902/stories/2.txt', encoding='utf8').read()
    corpus = story.split()

    ##DESC CONTD##
    description = secondOrderMarkov(corpus, 40).rsplit('.',1)
    final_desc = description[0].replace('ZORP', random.choice(characters))+"."


    ##DIALOGUE CONTD##
    dialogue_1 = dialogue_gen("SB1902/dialogue.txt", random.randint(8,20))

    dialogue_2  = dialogue_gen("SB1902/dialogue.txt", random.randint(8,20))

    ##ACTION GEN##
    with open('SB1902/parts of speech word files/present_tense.csv') as f:
        present_tense = list(f)[0]

    with open('SB1902/parts of speech word files/adverbs.csv') as a:
        adverbs = list(a)

    ly_adverbs = []
    for i in adverbs:
        i.split('\n')
        if i.endswith('ly\n'):
            ly_adverbs = np.append(ly_adverbs, i.lower()[:-1] )
        else:
            pass

    present_list = present_tense.split(',')
    action = character1+" "+random.choice(present_list)+" "+random.choice(ly_adverbs)   

    ##IMG COMPILER##
    ##structure
    img = Image.new('RGB', (500,500), color = "white")
    fnt = ImageFont.truetype('SB1902/Courier New Bold.ttf', 15)
    l = ImageDraw.Draw(img)
    l.text((25,25), location.upper(), font=fnt, fill=(0, 0, 0))

    desc = textwrap.wrap(final_desc, width=50)
    y_desc = 70

    for d in desc:
        width, height = fnt.getsize(d)
        l.text((25, y_desc), d, font=fnt, fill=(0,0,0))
        y_desc += height

    ## Structure Randomizer
    elements=['cd1'] * 35 + ['cd2'] * 35 + ['a'] * 30

    structure = list(['','','','',''])

    for i in np.arange(len(structure)): 
        structure[i] = random.choice(elements)
        while structure[i]==structure[i-1]:
            structure[i] = random.choice(elements)

    # Structure Applicator

    for i in np.arange(len(structure)):
        output = []
        y_mod = i*60
        if structure[i] == 'cd1':
            l.text((200,160 + y_mod), character1, font=fnt,fill=(0,0,0))

            dia1 = textwrap.wrap(dialogue_gen("SB1902/stories/final_dialogu.txt", random.randint(10,18)), width=45)
            y_dia1 = 180 + y_mod

            for d in dia1:
                width, height = fnt.getsize(d)
                l.text((45, y_dia1), d, font=fnt, fill=(0,0,0))
                y_dia1 += height
        elif structure[i] == 'cd2':
            l.text((200,160 + y_mod), character2, font=fnt,fill=(0,0,0))

            dia2 = textwrap.wrap(dialogue_gen("SB1902/stories/final_dialogu.txt", random.randint(10,18)), width=45)
            y_dia2 = 180 + y_mod

            for d in dia2:
                width, height = fnt.getsize(d)
                l.text((45, y_dia2), d, font=fnt, fill=(0,0,0))
                y_dia2 += height
        else:
            l.text((80,175+y_mod), random.choice(characters)+" "+random.choice(present_list)+" "+random.choice(ly_adverbs), font=fnt,fill=(0,0,0)) 
    save_file = 'SB1902/timed_hop/script_'+location.replace(' ', "").replace('-', "").replace('/', "")+"_"+character1+"_"+character2+'.png'
    img.save(save_file)
    output=post_to_fb(location.upper()+": "+character1+", "+character2, save_file)
    return output

def timer(hours):
    starttime=time.time()
    posts=[]
    i = 0
    while i <= hours:
        script_runner()
        time.sleep((30.0) - ((time.time() - starttime) % (30.0)))
        script_runner()
        posts = np.append(posts, 'post')
        time.sleep((86400.0) - ((time.time() - starttime) % (86400.0)))
        i += 1
    return len(posts)
print('initialized: timer')

timer(1000)

print('terminated: action')
