# -*- coding: utf-8 -*-
"""Project 1 Heart Disease System

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19H2EeB5PIr74N7s0QKos_ZOTFP8KFivF

# Imports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from mlxtend.plotting import plot_decision_regions
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout

"""# Getting and Cleaning the Data- EDA"""

from google.colab import files
uploaded = files.upload()

df = pd.read_csv('heart.csv')

df.head()

df.info()

df.head()

"""### Normalization/Standardization
Standardizing features by removing mean and scaling to unit variance
"""

scaler = StandardScaler()
scalable_columns = ["age", "trestbps", "chol", "thalach", "oldpeak"]
df[scalable_columns] = scaler.fit_transform(df[scalable_columns])

df.info()

df.head()

"""# Data Visualization"""

import missingno as msn
msn.matrix(df)

df.hist(figsize = (20,20),color='#ADFF2F')
plt.tight_layout()
plt.show()

df['target'].value_counts()

Hdislabel = ['Have heart disease','Do not have heart disease'] #2 categories of data
val_counts = [165,138] # values of 2 categories
#pie figure draw
fig = px.pie(values=val_counts,names=Hdislabel, #assigning value= count value as we wook [508,409] & #names=will be returned by the Hdislabel function
             color=Hdislabel, #labeled colour to pie chart
             color_discrete_map={'Have heart disease':'#FF4500',  #adding colour to pie chart
                                 'Do not have heart disease':'#FFFF00'},
             title='Heart disease count') #top title to pie figure

fig.show() #display figure

import seaborn as sns
import matplotlib.pyplot as plt
ax = sns.countplot(x="sex", data=df)

for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width()/2, height+0.3,'{:.0f}'.format(height), ha="center")

print(f"{len(df[(df['sex']==1) & (df['target']==1)])} male")
print(f"{round(len(df[(df['sex']==1) & (df['target']==1)])/len(df[df['sex']==1])*100,2)}% of male are diagnosed to have heart disease among 207 male")

plt.figure(figsize=(20,20))
from pandas.plotting import scatter_matrix
p=scatter_matrix(df,figsize=(25, 25))

p=sns.pairplot(df, hue = 'target')

plt.figure(figsize = (20, 20))
sns.heatmap(df.corr(),annot=True)
plt.title('Fig: Annoted values of correlation coefficient of each pair of features', y=-0.23)



"""# Models"""

df["target"]

y = df["target"]
X = df.drop(["target"], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""## KNN

"""

knn_scores=[]
for k in range(1,40):
  knn_classifier=KNeighborsClassifier(n_neighbors=k)
  knn_classifier.fit(X_train,y_train)
  knn_scores.append(knn_classifier.score(X_test,y_test))

best_choice_for_k = np.argmax(knn_scores)+1
print(f'Best choice of k : {best_choice_for_k}')

knn_classifier=KNeighborsClassifier(n_neighbors=best_choice_for_k)
knn_classifier.fit(X_train,y_train)
y_pred=knn_classifier.predict(X_test)
print(f'Accuracy:{np.sum(y_pred==y_test)/len(y_test)}')

"""## SVM"""

svc_scores = []
kernels = ['linear','poly','rbf','sigmoid']
for i in range(len(kernels)):
  svc_scores_c=[]
  for ch in range(1,11):
    if kernels [i]=='poly':
      svc_scores_poly=[]
      for d in range(3,10):
        svc_classifier = SVC(kernel =kernels[i], C=ch, degree=d)
        svc_classifier.fit(X_train, y_train)
        svc_scores_poly.append(svc_classifier.score(X_test,y_test))
      print(f'Best polynomial score: {np.argmax(svc_scores_poly)+3}')
      svc_scores_c.append(svc_scores_poly[np.argmax(svc_scores_poly)])
    else:
      svc_classifier = SVC(kernel = kernels[i], C=ch)
      svc_classifier.fit(X_train, y_train)
      svc_scores_c.append(svc_classifier.score(X_test, y_test))
  print(f'Best choice of c for {kernels[i]}: {np.argmax(svc_scores_c)+1}')
  svc_scores.append(svc_scores_c[np.argmax(svc_scores_c)])
print(f'Best choice of k: {kernels[np.argmax(svc_scores)]}')

svc_classifier = SVC(kernel="rbf", C=1)
svc_classifier.fit(X_train, y_train)
print(svc_classifier.score(X_test, y_test))

"""## Decision Tree"""

dt_scores=[]
cr_scores=[]
for cr in ['gini','entropy']:
  for i in range(1, len(X.columns)+1):
    dt_classifier = DecisionTreeClassifier(criterion=cr, max_features=i, random_state=42)
    dt_classifier.fit(X_train, y_train)
    dt_scores.append(dt_classifier.score(X_test, y_test))
  print(f'Best max_features for{cr}:{np.argmax(dt_scores)+1}')
  cr_scores.append(dt_scores[np.argmax(dt_scores)])
print(f'Best criterion:{"gini" if not np.argmax(cr_scores) else "entropy"}')

from pandas.core.common import random_state
dt_classfier=DecisionTreeClassifier(criterion='gini',max_features=14, random_state=42)
dt_classifier.fit(X_train,y_train)
print(dt_classifier.score(X_test,y_test))

"""## Random Forest"""

print('RandomForestClassifier')
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100) # , max_depth=5, random_state=1
model.fit(X_train, y_train)
Y_pred = model.predict(X_test)
score = model.score(X_train, y_train)
print('Training Score:', score)
score = model.score(X_test, y_test)
print('Testing Score:', score)
output = pd.DataFrame({'Predicted':Y_pred}) # Heart-Disease yes or no? 1/0
print(output.head())
people = output.loc[output.Predicted == 1]["Predicted"]
rate_people = 0
if len(people) > 0 :
    rate_people = len(people)/len(output)
print("% of people predicted with heart-disease:", rate_people)
score_rfc = score
out_rfc = output
from sklearn.metrics import classification_report
print(classification_report(y_test,Y_pred))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test,Y_pred)
class_names = [0,1]
fig,ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks,class_names)
plt.yticks(tick_marks,class_names)
sns.heatmap(pd.DataFrame(confusion_matrix), annot = True, cmap = 'Greens', fmt = 'g')
ax.xaxis.set_label_position('top')
plt.tight_layout()
plt.title('Confusion matrix for random forest')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.show()

# ROC Curve
from sklearn.metrics import roc_auc_score,roc_curve
y_probabilities = model.predict_proba(X_test)[:,1]
false_positive_rate, true_positive_rate, threshold_knn = roc_curve(y_test,y_probabilities)
plt.figure(figsize=(10,6))
plt.title('ROC for random forest')
plt.plot(false_positive_rate, true_positive_rate, linewidth=5, color='green')
plt.plot([0,1],ls='--',linewidth=5)
plt.plot([0,0],[1,0],c='.5')
plt.plot([1,1],c='.5')
plt.text(0.2,0.6,'AUC: {:.2f}'.format(roc_auc_score(y_test,y_probabilities)),size= 16)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.show()

"""## ANN"""

model = Sequential([
    Dense(20, activation="relu"),
    Dropout(0.2),
    Dense(25, activation="relu"),
    Dense(45, activation="relu"),
    Dropout(0.5),
    Dense(10, activation="relu"),
    Dense(2, activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

early_stop = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=5)
batches = 32
nr_epochs = 500

model.fit(X_train, y_train, batch_size=batches, epochs = nr_epochs)

model.evaluate(X_test, y_test, batch_size=32)

"""##Naive Bayes"""

from sklearn.naive_bayes import GaussianNB

gaussNB = GaussianNB()

# Training our model

gaussNB.fit(X_train,y_train)

Y_pred_nb = gaussNB.predict(X_test)

from sklearn.metrics import accuracy_score
print('The value of accuracy score is ',accuracy_score(y_test,Y_pred_nb))

"""#CONCLUSION

KNN works best (88.52% accuracy). So we'll use KNN

#DEPLOY MODEL
"""

import pickle                                                                                                                                          #library needed for saving the model

filename = 'trained_model.sav'                                                                                                             #new variable with a new file saved in that variable
pickle.dump(knn_classifier, open(filename, 'wb'))                                                                                                   #model is loaded in knn coz of best accuracy
                                                                                                                                                                                 # write bianry

loaded_model = pickle.load(open('trained_model.sav', 'rb'))                                                                                                        #load and read binary file

input_data = (5,166,72,19,175,25.8,0.587,51,92,88.09,17,121.22,100)

input_data_as_numpy_array = np.asarray(input_data)                                                                                                              #input to numpy array

input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)                                                                                                     #predicting one instance

prediction = loaded_model.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('The person is not diagnosed with Heart Disease')
else:
  print('The person is diagnosed with Heart Disease')

