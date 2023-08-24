import pandas as pd
import re

train=pd.read_csv('final_train.csv')

train.shape

train.drop_duplicates()

train.dropna()

train.head()

train.info()

X=train['message']
Y=train['Language']

keyword=[]
for text in X:
  text = re.sub(r'[1@#$(),%^*?:;~0-9]',' ', text)
  text.lower()
  keyword.append(text)
  
from sklearn.feature_extraction.text import CountVectorizer
cv= CountVectorizer()
X=cv.fit_transform(keyword)

from sklearn.preprocessing import LabelEncoder

le=LabelEncoder()
Y = le.fit_transform(Y)

Y

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.3, random_state=42)


from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def training(model):
  clf = model().fit(X_train,Y_train)
  train_acc = accuracy_score(Y_train, clf.predict(X_train))
  test_acc = accuracy_score(Y_test, clf.predict(X_test))
  print(train_acc, test_acc)
  return clf

svc = training(LinearSVC)

str_in = ["Hello I am Abhay"] # it should always be in array format
str_in = cv.transform(str_in)
str_in

re = le.inverse_transform(svc.predict(str_in))
re[0]

#!pip install streamlit -q

%%writefile app.py
import streamlit as st
import re
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import  accuracy_score


@st.cache_data
def main():
  train = pd.read_csv(r"/content/final_train.csv")
  train = train.drop_duplicates()
  train = train.dropna()
  X = train['message']
  Y = train['Language']
  keyword =[]
  for text in X:
    text = re.sub(r'[1@#$(),%^*?:;~0-9]',' ', text)
    text = text.lower()
    keyword.append(text)
  cv = CountVectorizer()
  X = cv.fit_transform(keyword)
  le = LabelEncoder()
  Y=le.fit_transform(Y)
  X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.3, random_state=42)
  model = LinearSVC().fit(X_train,Y_train)

  return model, cv, le


# streamlit code
st.set_page_config(page_title='Multilingual Language System', page_icon='📚',layout='centered', initial_sidebar_state='auto')
st.title('Multilingual Language System')
st.spinner('Loading...')

model, cv, le = main()

#Language Sentence input
user_text = st.text_input('Enter The Text -->', label_visibility='visible', disabled=False, max_chars=None, key=None, type='default')

result=[]
with st.form("Form", clear_on_submit=True):
  submitted = st.form_submit_button('Submit', disabled=not(user_text))
  if submitted:
    with st.spinner('Predicting...'):
      text=[]
      text.append(user_text)
      text= cv.transform(text)
      res= le.inverse_transform(model.predict(text))
      result.append(res[0])

if len(result):
  with st.spinner('Predicting...'):
    st.info(f'Predicted Language is {result[0]}')
    
    
!streamlit run app.py & npx localtunnel --port 8501