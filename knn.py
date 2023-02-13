import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

#load data from goodreads 10k dataset
books = pd.read_csv('data/books.csv')
ratings = pd.read_csv('data/ratings.csv')

#remove all positions with missing values from books
books = books.dropna()
#remove duplicates
ratings.drop_duplicates(subset=["user_id","book_id"], keep='first', inplace=True)
books.drop_duplicates(subset='original_title', keep='first', inplace=True)

#sort ratings by user_id
ratings = ratings.sort_values("user_id")

#df int dataframe
df = pd.merge(books, ratings, how='left', left_on=['id'], right_on=['book_id'])
books_ratings = df[['id','original_title', 'user_id', 'rating', 'image_url', 
'average_rating', 'isbn', 'authors', 'original_publication_year', 'ratings_count']]
books_ratings = books_ratings.rename(columns = {'id':'book_id'})

#orginal dataframe with selected columns to display float values in app
books_ratings_org = books_ratings[['book_id','average_rating','original_publication_year', 'ratings_count']]

#change type to int gain performance on computing models
books_ratings_df = books_ratings.astype(np.int8,errors='ignore')

#fill missing ratings values with 0; NearestNeighbors does not accept missing values encoded as NaN
ratings_df = books_ratings_df.pivot_table(index='book_id',columns='user_id',values='rating').fillna(0)

#create model (int in this case is enough)
model_knn = NearestNeighbors(metric='cosine', algorithm = 'auto')
model_knn.fit(ratings_df.values)


def get_book_id(book_title):
    """
    function to get book_id from books_ratings

    :param book_title: book title to get id
    :return: Pandas Series
    """
    df = books_ratings_df.loc[books_ratings_df['original_title'] == book_title]
    return df['book_id'].iloc[0]

def get_recomm_knn(book_title, num_neighbors=10): 
    """
    recommend by computing lowest distance

    :param title: book title to get recommendations
    :int num_neighbors: number of neighbors in KNN (and also number of recommendations to display)
    :return: list with book_ids
    """ 
    book_list = []
    query_index = get_book_id(book_title)
    
    if num_neighbors > 0:
        distances, indices = model_knn.kneighbors(ratings_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = num_neighbors + 1)
    else:
        distances, indices = model_knn.kneighbors(ratings_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 10 + 1)
    
    for i in range(0, len(distances.flatten())):
        book_list.append(ratings_df.index[indices.flatten()[i]])
    
    return book_list
        