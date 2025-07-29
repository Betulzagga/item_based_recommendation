###########################################
# Item-Based Collaborative Filtering
###########################################

# Veri seti: https://grouplens.org/datasets/movielens/

# Adım 1: Veri Setinin Hazırlanması
# Adım 2: User Movie Df'inin Oluşturulması
# Adım 3: Item-Based Film Önerilerinin Yapılması
# Adım 4: Çalışma Scriptinin Hazırlanması

######################################
# Adım 1: Veri Setinin Hazırlanması
######################################
import pandas as pd
pd.set_option('display.max_columns', 500)
movie = pd.read_csv('/Users/betulzagga/Library/Application Support/JetBrains/PyCharm2024.3/extensions/com.intellij.database/data/movie.csv')
rating = pd.read_csv('/Users/betulzagga/Library/Application Support/JetBrains/PyCharm2024.3/extensions/com.intellij.database/data/rating.csv')
df = movie.merge(rating, how="left", on="movieId")
df.head()

#film isimleri id, film turleri, puanlari, tarihler var
#amacimiz bir film verildiginde benzer begenilme ihtimalli filmler gostermek

######################################
# Adım 2: User Movie Df'inin Oluşturulması
######################################

#temel amacimiz bu data frame i olusturmak
#kullanici geldi bir puan verdi diger vermedigi filmlere de df olusturagiz indirgeme yapmamiz gerek
#matrixin on binlerce puani var, cok az oy olanlarla isimiz yok, analiz de masrafli, daha az da alt kume olusturulur
#analize baslamadan once binden az yorum puan almis filmeri indirgeriz
df.head()
df.shape

df["title"].nunique()
#essiz kac film var?

df["title"].value_counts().head()
#gercekten hepsine odaklancak miyiz?
#titlerin countini alirsak filmlere ve onlara verilmmis puanlari buluruz
comment_counts = pd.DataFrame(df["title"].value_counts())
#her bir filmde kac tane value count var onu pd df ile atiyorum df den secim ypiyorum donusturmeden dolayi oyle gorunuyo
#rare_movies = comment_counts[comment_counts["title"] <= 1000].index ----bu kod hata verdi
#Çünkü string ile sayı karşılaştırılamaz.
#benim yapmak istediğim aslında yorum sayısı 1000’den az olan filmlerin isimlerini almak olabilir.
#Bunun için önce groupby()
comment_counts = df.groupby("title").size()
rare_movies = comment_counts[comment_counts <= 1000].index

#satirlari getirir, 24103 tane film 1000 az rate e  sahip
#index dersem isimleri gelir, ben bunlari rare olarak kaydedip onlari cikartacagim
common_movies = df[~df["title"].isin(rare_movies)]
#rare icindekilere bak bunun disindakileri sec diyorum
common_movies.shape
common_movies["title"].nunique()
df["title"].nunique()

#indirgeme islemini tamamladik, bu df oyle bi islem yapacagiz ki satirlarda kullanicilar, sutunlarda title yani pivot islemi yapacagiz
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")

#index user id, sutunlarda film title kesisimler rating al
#kume biraz daha kuculsun istersem 10bine indirgeyebiliriz

user_movie_df.shape

user_movie_df.columns


######################################
# Adım 3: Item-Based Film Önerilerinin Yapılması
######################################
#cesitli korelasyon islemleri yapmamiz gerekiyor
#bir film ile diger filmler arasinda korelasyonuna bakacagiz
movie_name = "Matrix, The (1999)"
movie_name = "Ocean's Twelve (2004)"
movie_name = user_movie_df[movie_name]
#degisken secme islemi gibi yapiyoruz (eskisiyle ilgilenmiyorum)

user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)


movie_name = pd.Series(user_movie_df.columns).sample(1).values[0]
movie_name = user_movie_df[movie_name]
user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)


def check_film(keyword, user_movie_df):
    return [col for col in user_movie_df.columns if keyword in col]

check_film("Insomnia", user_movie_df)


######################################
# Adım 4: Çalışma Scriptinin Hazırlanması
######################################

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()


def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)

item_based_recommender("Matrix, The (1999)", user_movie_df)

movie_name = pd.Series(user_movie_df.columns).sample(1).values[0]

item_based_recommender(movie_name, user_movie_df)





