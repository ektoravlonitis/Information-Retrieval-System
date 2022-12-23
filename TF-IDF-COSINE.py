#THE ISLANDERS

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import csv

file = open('Lyrics.csv', 'r')

df = pd.read_csv ('Lyrics.csv', names=['song','artist','lyrics'],sep=',', skiprows=1, encoding='latin-1')
porter = PorterStemmer()

docs = []
documents = []
for i in df['lyrics']:
    documents += [i]
    line = i.strip()
    tokens = word_tokenize(line)
    words = [word.lower() for word in tokens if word.isalpha()]
    tokens_without_sw = [word for word in words if not word in stopwords.words('english')]
    stemmed = [porter.stem(word) for word in tokens_without_sw]
    lyric = (" ").join(tokens_without_sw)
    docs += [lyric]

songs = []
for i in df['song']:
    songs += [i]

artists = []
for i in df['artist']:
    artists += [i]

# Create a TfidfVectorizer object
vectorizer = TfidfVectorizer()
# Fits the data and transform it to a vector
X = vectorizer.fit_transform(docs)
# Convert X to transposed matrix
X = X.T.toarray()
# Create a DataFrame and set the vocabulary as the index
df2 = pd.DataFrame(X, index=vectorizer.get_feature_names_out())

def get_similar_lyrics(q, df2):
  print("query:", q)
  print("The following are lyrics with the highest cosine similarity values: ")
  # Convert the query become a vector
  q = [q]
  q_vec = vectorizer.transform(q).toarray().reshape(df2.shape[0],)
  sim = {}
  # Calculate the similarity
  for i in range(df2.shape[1]):
      sim[i] = np.dot(df2.loc[:, i].values, q_vec) / np.linalg.norm(df2.loc[:, i]) * np.linalg.norm(q_vec)
  
  # Sort the values 
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
  print(sim_sorted)
  # Print the lyrics and their similarity values
  x = 0
  result = open('Lyrics_after_tfidf.csv', "a", encoding="utf-8")
  fieldnames = ['song', 'artist', 'lyrics']
  writer = csv.DictWriter(result, fieldnames=fieldnames)
  writer.writeheader()
  last_v = 0.0
  for k, v in sim_sorted:
    if v != 0.0:
      if v!= last_v:
          last_v = v
          print("Similarity Value:", v)
          writer.writerow({'song': songs[k], 'artist': artists[k], 'lyrics': documents[k]})
          #sbert += [documents[k]]
          x += 1
          if x == 50:
              break;
          print(documents[k])
          print()
      else:
          continue

# Add The Query
q1 = 'love and peace'

line = q1.strip()
tokens = word_tokenize(line)
words = [word.lower() for word in tokens if word.isalpha()]
tokens_without_sw = [word for word in words if not word in stopwords.words('english')]
stemmed = [porter.stem(word) for word in tokens_without_sw]
q1 = (" ").join(stemmed)

# Call the function
get_similar_lyrics(q1, df2)