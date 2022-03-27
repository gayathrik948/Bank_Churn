import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score as f1
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score
from imblearn.over_sampling import SMOTE


data = pd.read_excel('CHURNDATA.xlsx')
df = data.copy()

del df['CIF']
del df['CUS_DOB']
del df['CUS_Customer_Since']

df.isnull().sum()

df.dropna(subset = ['CUS_Month_Income'], inplace=True)
df.dropna(subset = ['CUS_Gender'], inplace=True)

label_encoder = LabelEncoder()
df['Status']= label_encoder.fit_transform(df['Status'])

df.describe()

x = df.iloc[:, :-1]
y = df.iloc[:, -1]

x['TAR_Desc'] = label_encoder.fit_transform(x['TAR_Desc'])
x['CUS_Gender'] = label_encoder.fit_transform(x['CUS_Gender'])
x = pd.get_dummies(x, drop_first=True)

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=0, stratify=y)

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(x_train, y_train)
y_pred = rf.predict(x_test)
print(accuracy_score(y_test, y_pred))
print(recall_score(y_test, y_pred))
print(precision_score(y_test, y_pred))
print(f1(y_test, y_pred))

x_1, y_1 = SMOTE().fit_resample(x,y)

x_train1, x_test1, y_train1, y_test1 = train_test_split(x_1,y_1, test_size=0.2, random_state=0, stratify=y_1)

rf.fit(x_train1, y_train1)
y_pred1 = rf.predict(x_test1)
print(accuracy_score(y_test1, y_pred1))
print(recall_score(y_test1, y_pred1))
print(precision_score(y_test1, y_pred1))
print(f1(y_test1, y_pred1))

import pickle
pickle.dump(rf, open("model_churn.sav", "wb"))

model = pickle.load(open("model_churn.sav", "rb"))
print(model.predict([[30,2500000,1,14,135,76,36,764270.6,929922.75,592449,7,28,11,187800,490056,
                     369480,2286642.3,247,1047336,46,293,2222,2,0,0,1,0,0]]))