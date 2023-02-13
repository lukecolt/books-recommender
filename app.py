import streamlit as st
from PIL import Image
import io
import PIL.Image
from urllib.request import urlopen
import pandas as pd
from knn import *
from cossim import *

def get_title(df, book_id):
    """
    function to get title from book_id

    :param df: working dataframe
    :param book_id: book_id to get title
    :return: Pandas Series
    """
    target_df = df.loc[df['book_id'] == book_id]
    return target_df['original_title'].iloc[0]

def get_link(df, book_id):
    """
    function to get link from book_id

    :param df: working dataframe
    :param book_id: book_id to get link
    :return: Pandas Series
    """
    target_df = df.loc[df['book_id'] == book_id]
    return target_df['image_url'].iloc[0]

def get_av_rat(df,df_avr, book_id):
    """
    function to get average rating from book_id

    :param df: working dataframe
    :param book_id: book_id to get average rating
    :return: Pandas Series
    """
    target_df = df_avr.loc[df['book_id'] == book_id]
    return target_df['average_rating'].iloc[0]

def get_isbn(df, book_id):
    """
    function to get ISBN number from book_id

    :param df: working dataframe
    :param book_id: book_id to get ISBN number
    :return: Pandas Series
    """
    target_df = df.loc[df['book_id'] == book_id]
    return target_df['isbn'].iloc[0]

def get_authors(df, book_id):
    """
    function to get authors from book_id

    :param df: working dataframe
    :param book_id: book_id to get authors
    :return: Pandas Series
    """
    target_df = df.loc[df['book_id'] == book_id]
    return target_df['authors'].iloc[0]

def get_year(df,df_avr, book_id):
    """
    function to get publication year from book_id

    :param df: working dataframe
    :param df_avr: dataframe to display real-value data
    :param book_id: book_id to get publication year
    :return: Pandas Series
    """
    target_df = df_avr.loc[df['book_id'] == book_id]
    return target_df['original_publication_year'].iloc[0]

def get_rat_count(df,df_avr, book_id):
    """
    function to get ratings count year from book_id

    :param df: working dataframe
    :param df_avr: dataframe to display real-value data
    :param book_id: book_id to get ratings count
    :return: Pandas Series
    """
    target_df = df_avr.loc[df['book_id'] == book_id]
    return target_df['ratings_count'].iloc[0]

def movie_poster_fetcher(url):
    """
    function to load image from url

    :param book_title: goodreads image url
    """
    u = urlopen(url)
    raw_data = u.read()
    image = PIL.Image.open(io.BytesIO(raw_data))
    st.image(image, use_column_width=False)

def run():
    """
    function to run streamlit app
    """
    st.set_page_config(page_title='Book Recommender', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
    st.title("Books Recommender System")
    st.markdown('''<h6 style='text-align: left;'>Select recommendation type and book title to get recommendations</h6>''',
                unsafe_allow_html=True)
    st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Data is based on "Goodreads 10000 Dataset"</h5>''',
                unsafe_allow_html=True)
    titles = books['original_title'].values.tolist()
    category = ['--Select--', 'K-NN (k-Nearest Neighbor)', 'Cosine similarity']
    cat_op = st.selectbox('Select Recommendation Type', category)
    if cat_op == category[0]:
        st.warning('Please select Recommendation Type!!')
    #KNN
    elif cat_op == category[1]:
        select_book = st.selectbox('Select (or start writing in dropdown list below) book title: (Recommendation will be based on this selection)', ['--Select or Write--'] + titles)
        dec = st.radio("Want to fetch book cover?", ('Yes', 'No'))
        if dec == 'No':
            if select_book == '--Select or Write--':
                st.warning('Please select movie!!')
            else:
                no_of_reco = st.slider('Number of books to recommended:', min_value=5, max_value=20, step=1)
                table = get_recomm_knn(select_book, num_neighbors=no_of_reco)
                table.pop(0)
                c = 0
                st.success('List of: ' + str(no_of_reco) + ' recommendations, have a look below')
                for b in table:
                      c+=1
                      st.subheader(f"{c}" + ". "+ get_title(books_ratings_df, b))
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Author(s): ''' + get_authors(books_ratings_df, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>ISBN number: ''' + get_isbn(books_ratings_df, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Average rate (1-5): ''' + str(get_av_rat(books_ratings_df,books_ratings_org, b)),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>Publication year: ''' + str(int(get_year(books_ratings_df,books_ratings_org, b))),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Number of ratings: ''' + str(get_rat_count(books_ratings_df,books_ratings_org, b)),
                            unsafe_allow_html=True)
        else:
            if select_book == '--Select or Write--':
                st.warning('Please select book!!')
            else:
                no_of_reco = st.slider('Number of books to recommended:', min_value=5, max_value=20, step=1)
                table = get_recomm_knn(select_book, num_neighbors=no_of_reco)
                table.pop(0)
                c = 0
                st.success('List of: ' + str(no_of_reco) + ' recommendations, have a look below')
                for b in table:
                      c+=1
                      st.subheader(f"{c}" + ". "+ get_title(books_ratings_df, b))
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Author(s): ''' + get_authors(books_ratings_df, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>ISBN number: ''' + get_isbn(books_ratings_df, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Average rate (1-5): ''' + str(get_av_rat(books_ratings_df,books_ratings_org, b)),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>Publication year: ''' + str(int(get_year(books_ratings_df,books_ratings_org, b))),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Number of ratings: ''' + str(get_rat_count(books_ratings_df,books_ratings_org, b)),
                            unsafe_allow_html=True)
                      movie_poster_fetcher(get_link(books_ratings_df, b))

    #Cosine similarity
    elif cat_op == category[2]:
        select_book = st.selectbox('Select (or start writing in dropdown list below) book title: (Recommendation will be based on this selection)', ['--Select or Write--'] + titles)
        
        dec = st.radio("Want to fetch book cover?", ('Yes', 'No'))
        if dec == 'No':
            if select_book == '--Select or Write--':
                st.warning('Please select book!!')
            else:
                no_of_reco = st.slider('Number of books to recommended:', min_value=5, max_value=20, step=1)
                table = get_recomm_cos_sim(select_book, cosine_sim, n_sim=no_of_reco)
                table.pop(0)
                c = 0
                st.success('List of: ' + str(no_of_reco) + ' recommendations, have a look below')
                for b in table:
                      c+=1
                      st.markdown(f"({c})")
                      st.subheader(f"{c}" + ". "+ get_title(cos_sim_data, b))
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Author(s): ''' + get_authors(cos_sim_data, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>ISBN number: ''' + get_isbn(cos_sim_data, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Average rate (1-5): ''' + str(get_av_rat(cos_sim_data,cos_sim_data, b)),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>Publication year: ''' + str(int(float(get_year(cos_sim_data, cos_sim_data, b)))),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Number of ratings: ''' + str(get_rat_count(cos_sim_data,cos_sim_data, b)),
                            unsafe_allow_html=True)
        else:
            if select_book == '--Select or Write--':
                st.warning('Please select book!!')
            else:
                no_of_reco = st.slider('Number of books to recommended:', min_value=5, max_value=20, step=1)
                table = get_recomm_cos_sim(select_book, cosine_sim, n_sim=no_of_reco+1)
                table.pop(0)
                c = 0
                st.success('List of: ' + str(no_of_reco) + ' recommendations, have a look below')
                for b in table:
                      c+=1
                      st.subheader(f"{c}" + ". "+ get_title(cos_sim_data, b))
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Author(s): ''' + get_authors(cos_sim_data, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>ISBN number: ''' + get_isbn(cos_sim_data, b),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Average rate (1-5): ''' + str(get_av_rat(cos_sim_data,cos_sim_data, b)),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left;'>Publication year: ''' + str(int(float(get_year(cos_sim_data, cos_sim_data, b)))),
                            unsafe_allow_html=True)
                      st.markdown('''<h5 style='text-align: left; color: #d73b5c;'>Number of ratings: ''' + str(get_rat_count(cos_sim_data,cos_sim_data, b)),
                            unsafe_allow_html=True)
                      movie_poster_fetcher(get_link(cos_sim_data, b))
run()