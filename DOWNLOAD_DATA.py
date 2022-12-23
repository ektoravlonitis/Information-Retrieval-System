# THE ISLANDERS

import urllib.request, urllib.parse, urllib.error
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import random
import csv

# I set up a delay so that the website doesn't get suspicious of abnormal data collection
delay = 30
url = "https://www.azlyrics.com/"

# i use the beautiful soup library
# it is the same we used for the project and I am more familiar with it
r = requests.get(url)
soup = bs(r.content, "lxml")

# I opened the elements of the webiste and observed the html tags that need to be accessed
# with the code below I obtain the urls of the website articles
letters = []
g_data = soup.find_all("a", {"class": "btn btn-menu"})
for item in g_data:
    print(item.get("href"))
    letters += [item.get("href")]

new_letters=[]
for i in range(10):
    random_num = random.choice(letters)
    new_letters += [random_num]

#FIRST STEP
artists = []
for i in new_letters:
    try:
        url = "http:" + i
        r2 = requests.get(url)
        soup2 = bs(r2.content, "lxml")

        g_data2 = soup2.find_all("div", {"class": "col-sm-6 text-center artist-col"})
        for div in g_data2:
            links = div.find_all('a')
            for a in links:
                print(a['href'])
                artists += [a["href"]]
    except:
        print("error")
        break;
    finally:
        sleep(delay)

new_artists=[]
for i in range(40):
    random_num = random.choice(artists)
    new_artists += [random_num]


#SECOND STEP
songs = []
for i in new_artists:
    try:
        url = "https://www.azlyrics.com/" + i
        r3 = requests.get(url)
        soup2 = bs(r3.content, "lxml")

        g_data3 = soup2.find_all("div", {"class": "listalbum-item"})
        for div in g_data3:
            links = div.find_all('a')
            for a in links:
                print(a['href'])
                songs += [a["href"]]
    except:
        print("error")
        break;
    finally:
        sleep(delay)

new_songs=[]
for i in range(1500):
    random_num = random.choice(songs)
    new_songs += [random_num]

with open ('Lyrics!.csv', "a") as csvfile:
    fieldnames = ['song', 'artist', 'lyrics']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in new_songs:
        try:
            if i[0:5] == 'https':
                f_url=i
                html_page=urllib.request.urlopen(f_url).read()
                soup=bs(html_page, 'html.parser')
                html_pointer=soup.find('div',attrs={'class':'ringtone'})
                song_name=html_pointer.find_next('b').contents[0].strip()
                html_pointer2=soup.find('div',attrs={'class':'lyricsh'})
                artist_name=html_pointer2.find_next('b').contents[0].strip()
                artist_name = artist_name.replace(" Lyrics", "")
                print(artist_name)
                lyrics=html_pointer.find_next('div').text.strip()
                lyrics = " ".join(line.strip() for line in lyrics.splitlines())
                
                writer.writerow({'song': song_name, 'artist': artist_name, 'lyrics': lyrics})
                print("lyrics succesfully written to file for: " + song_name)
            else:
                f_url = "https://www.azlyrics.com" + i
                html_page=urllib.request.urlopen(f_url).read()
                soup=bs(html_page, 'html.parser')
                html_pointer=soup.find('div',attrs={'class':'ringtone'})
                song_name=html_pointer.find_next('b').contents[0].strip()
                html_pointer2=soup.find('div',attrs={'class':'lyricsh'})
                artist_name=html_pointer2.find_next('b').contents[0].strip()
                artist_name = artist_name.replace(" Lyrics", "")
                print(artist_name)
                lyrics=html_pointer.find_next('div').text.strip()
                lyrics = " ".join(line.strip() for line in lyrics.splitlines())
                
                writer.writerow({'song': song_name, 'artist': artist_name, 'lyrics': lyrics})
                print("lyrics succesfully written to file for: " + song_name)
                
        except:
            print("lyrics not found for : ", i)
    
        finally:
            sleep(delay)