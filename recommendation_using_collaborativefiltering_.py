# -*- coding: utf-8 -*-
"""recommendation_using_collaborativefiltering .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17ZQS1W08yoUBPpafwHc8lc7yH1bGt__-
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import warnings
import os
import importlib
warnings.filterwarnings("ignore")
sns.set_theme(color_codes=True)

def check_and_install_library(library_name):
  try:
    importlib.import_module(library_name)
    print(f"{library_name} is already installed.")
  except ImportError:
    print(f"{library_name} is not installed. Installing....")
    try:
        import pip
        pip.main(["install",library_name])
    except:
      print("error: failed to install the library. please install it manually.")

if 'rating_Electronics'not in os.listdir():
  check_and_install_library('opendatasets')
  import opendatasets as od
  od.download("https://www.kaggle.com/datasets/irvifa/amazon-product-reviews")

df=pd.read_csv("/content/amazon-product-reviews/ratings_Electronics.csv",names=['userId','productId','rating','timestamp'])

df

df.shape

df.columns

sample_data=df.sample(n=1564896,ignore_index=True)

del df

sample_data.head()

sample_data.info()

sample_data.drop('timestamp',axis=1,inplace=True)

sample_data.describe()

sample_data.isnull().sum()

sample_data[sample_data.duplicated()].shape[0]

sample_data.head()

plt.figure(figsize=(5,5))

sns.countplot(x='rating',data=sample_data)
plt.title("rating_calculated")
plt.xlabel("rating")
plt.ylabel("count")
plt.grid()
plt.show

print('total rarting :',sample_data.shape[0])
print('total unique users:',sample_data['userId'].unique().shape[0])
print('total unique products:',sample_data['productId'].unique().shape[0])

no_of_rated_products_per_user = sample_data.groupby(by='userId')['rating'].count().sort_values(ascending=False)

no_of_rated_products_per_user.head()

print('no of rated products more than 50 per user:{}'.format(sum(no_of_rated_products_per_user >= 50)))

data=sample_data.groupby("productId").filter(lambda x:x['rating'].count() >=50)

data.head()

no_of_rated_products_per_user=data.groupby('productId')['rating'].count().sort_values(ascending=False)

no_of_rated_products_per_user.head(20).plot(kind='bar')

mean_rating_product_count = pd.DataFrame(data.groupby('productId')['rating'].mean())

plt.hist(mean_rating_product_count['rating'],bins=100)
plt.title("mean rating distribution")
plt.show()

mean_rating_product_count['rating'].skew()

mean_rating_product_count['rating_counts']= pd.DataFrame(data.groupby('productId')["rating"].count())

mean_rating_product_count.head()

mean_rating_product_count[mean_rating_product_count['rating_counts']== mean_rating_product_count['rating_counts'].max()]

print("min average rating product :",mean_rating_product_count['rating_counts'].min())

print("total min average rating products:",mean_rating_product_count[mean_rating_product_count['rating_counts']== mean_rating_product_count['rating_counts'].min()].shape[0])

plt.hist(mean_rating_product_count['rating_counts'],bins=100)
plt.title('rating count distribution')
plt.show()

sns.jointplot(x='rating',y='rating_counts',data=mean_rating_product_count)
plt.title('Joint Plot of rating and rating counts')
plt.tight_layout()
plt.show()

plt.scatter(x=mean_rating_product_count['rating'],y=mean_rating_product_count['rating_counts'])
plt.show()

print('Correlation between Rating and Rating Counts is : {} '.format(mean_rating_product_count['rating'].corr(mean_rating_product_count['rating_counts'])))

check_and_install_library('surprise')
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split

reader = Reader(rating_scale=(1, 5))
surprise_data = Dataset.load_from_df(data,reader)

trainset, testset = train_test_split(surprise_data, test_size=0.3,random_state=42)

algo = KNNWithMeans(k=5, sim_options={'name': 'pearson_baseline', 'user_based': False})
algo.fit(trainset)

test_pred=algo.test(testset)

print("Item-based Model : Test Set")
accuracy.rmse(test_pred ,verbose=True)

data2=data.sample(20000)
ratings_matrix = data2.pivot_table(values='rating', index='userId', columns='productId', fill_value=0)
ratings_matrix.head()

ratings_matrix.shape

x_ratings_matrix=ratings_matrix.T
x_ratings_matrix.head()

x_ratings_matrix.shape

from sklearn.decomposition import TruncatedSVD
SVD = TruncatedSVD(n_components=10)
decomposed_matrix = SVD.fit_transform(x_ratings_matrix)
decomposed_matrix.shape

correlation_matrix = np.corrcoef(decomposed_matrix)
correlation_matrix.shape

x_ratings_matrix.index[10]

i="B00001P4ZH"
product_names=list(x_ratings_matrix.index)
product_id=product_names.index(i)
print(product_id)

correlation_product_ID = correlation_matrix[product_id]
correlation_product_ID.shape

correlation_matrix[correlation_product_ID>0.75].shape

recommend = list(x_ratings_matrix.index[correlation_product_ID > 0.75])
print("recomended products that are correeated:",recommend[:20])

