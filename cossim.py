import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#load data from goodreads 10k dataset
books = pd.read_csv('data/books.csv')
#remove all positions with missing values from books
books = books.dropna()
#remove duplicates
books.drop_duplicates(subset='original_title', keep='first', inplace=True)

#choose proper columns
cos_sim_data = books[['original_title','authors','average_rating','id', 'image_url', 'isbn', 'ratings_count', 'original_publication_year']]
cos_sim_data = cos_sim_data.rename(columns = {'id':'book_id'})
#creating string to combine meaningful data
cos_sim_data = cos_sim_data.astype(str)
cos_sim_data['result'] = cos_sim_data['original_title'] + ' ' + cos_sim_data['authors'] + ' ' + cos_sim_data['average_rating']
cos_sim_data = cos_sim_data.reset_index()

#create indices to get cos similarity
indices = pd.Series(cos_sim_data.index, index=cos_sim_data['original_title'])

#use vectorizer to remove stopwords and get TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(cos_sim_data['result'])
tfidf_matrix.shape

#calculate cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_recomm_cos_sim(title, similarity=cosine_sim, n_sim=10):
    """
    recommend by computing similarity and return list with results

    :param title: book title to get recommendations
    :param similarity: cosine similarity matrix
    :int n_sim: describe about parameter p3
    :return: list with book_ids
    """ 
    idx = indices[title]
    #get similarity scores for every pair of books with chosen book
    sim = list(enumerate(similarity[idx]))
    #sort books based by similarity values
    sim = sorted(sim, key=lambda x: x[1], reverse=True)

    #get n_sim most similar books
    if n_sim > 0:
        n = n_sim + 1
        sim = sim[1:n]
    else:    
        sim = sim[1:11]
    #create list to display data
    book_indices = [i[0] for i in sim]
    book_list = list(cos_sim_data['book_id'].iloc[book_indices])

    return book_list
