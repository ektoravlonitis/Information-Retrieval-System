#THE ISLANDERS

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import time
import faiss
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3')

file = open('Lyrics_after_tfidf.csv', 'r')

df = pd.read_csv ('Lyrics_after_tfidf.csv', names=['song','artist','lyrics'],sep=',', skiprows=1, encoding='latin-1')


df['doc_len'] = df['lyrics'].apply(lambda words: len(words.split()))
max_seq_len = np.round(df['doc_len'].mean() + df['doc_len'].std()).astype(int)
sns.distplot(df['doc_len'], hist=True, kde=True, color='b', label='doc len')
plt.axvline(x=max_seq_len, color='k', linestyle='--', label='max len')
plt.title('lyrics length'); plt.legend()
plt.show()

encoded_data = model.encode(df.lyrics.tolist())
encoded_data = np.asarray(encoded_data.astype('float32'))
index = faiss.IndexIDMap(faiss.IndexFlatIP(768))
index.add_with_ids(encoded_data, np.array(range(0, len(df))).astype(np.int64))
faiss.write_index(index, 'lyrics.index')

def fetch_lyric_info(dataframe_idx):
    info = df.iloc[dataframe_idx]
    meta_dict = dict()
    meta_dict['song'] = info['song']
    meta_dict['artist'] = info['artist']
    meta_dict['lyrics'] = info['lyrics'][:500]
    return meta_dict
    
def search(query, top_k, index, model):
    t=time.time()
    query_vector = model.encode([query])
    top_k = index.search(query_vector, top_k)
    print('>>>> Results in Total Time: {}'.format(time.time()-t))
    top_k_ids = top_k[1].tolist()[0]
    top_k_ids = list(np.unique(top_k_ids))
    results =  [fetch_lyric_info(idx) for idx in top_k_ids]
    return results


query="fighting for love and peace"
results=search(query, top_k=5, index=index, model=model)
print("\n")
for result in results:
    print('\t',result)