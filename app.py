## Flask
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import cross_val_score
from sklearn.metrics.pairwise import euclidean_distances
from subprocess import check_output
from flask import Flask
from flask_cors import CORS, cross_origin
import sys
app = Flask(__name__)
CORS(app)
print(sys.path)

## Reading file
df=pd.read_csv("C:/Users/Javeria/Downloads/FYP-Python/DATASET.csv",sep=",")
##Removing spaces
df['Major Subjects in Matric'] = df['Major Subjects in Matric'].astype(str).str.replace(' ', '')
df['Major in Intermediate'] = df['Major in Intermediate'].astype(str).str.replace(' ', '')
df['Favorite Subject'] = df['Favorite Subject'].astype(str).str.replace(' ', '')
df['Area of Interest'] = df['Area of Interest'].astype(str).str.replace(' ', '')
## features 
features = ['Major Subjects in Matric', 'Matric Percentage', 'Major in Intermediate', 'Intermediate Percentage',
           'Favorite Subject', 'Area of Interest']
for feature in features:
    df[feature] = df[feature].fillna('')

## making combined features row
def combined_features(row):
    return str(row['Major Subjects in Matric'])+" "+str(row['Matric Percentage'])+" "+str(row['Major in Intermediate'])+" "+str(row['Intermediate Percentage'])+" "+str(row['Favorite Subject'])+" "+str(row['Area of Interest'])
df["combined_features"] = df.apply(combined_features, axis =1)

## vectorizer
vectorizer = TfidfVectorizer(
                     binary=False,
#                      max_df=0.95, 
#                      min_df=0.15,
                     ngram_range = (1,2),use_idf = False, norm = None)
doc_vectors = vectorizer.fit_transform(df['combined_features'])
# cv.get_feature_names()


## Function for finding similarity
def comp_description(query, results_number=20):
        results=[]
        q_vector = vectorizer.transform([query])
        print("Comparable Description: ", query)
        results.append(cosine_similarity(q_vector, doc_vectors.toarray()))
        f=0
        elem_list=[]
        for i in results[:10]:
            for elem in i[0]:
                    #print("Review",f, "Similarity: ", elem)
                    elem_list.append(elem)
                    f+=1
            print("Most Similar to Given Input #" ,elem_list.index(max(elem_list)))
            print("Similarity: ", max(elem_list))
            if sum(elem_list) / len(elem_list)==0.0:
                print("No similar descriptions")
            else:
                print(df['combined_features'].loc[elem_list.index(max(elem_list)):elem_list.index(max(elem_list))])
                print(df['Current Domain'].loc[elem_list.index(max(elem_list))])
                global x
                x = (df['Current Domain'].loc[elem_list.index(max(elem_list))])

## Flask API
@app.route('/hello/',methods=['GET'])
@app.route('/hello/<name>',methods=['GET','POST'])
def hello(name):
    comp_description(name)
    return x  

if __name__ == '__main__':
    app.run()