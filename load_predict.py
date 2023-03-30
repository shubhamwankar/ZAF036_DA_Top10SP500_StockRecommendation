# -*- coding: utf-8 -*-
"""load_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17IpYu-Kk1cMt0A06zhON8EESjWO1EQ4m
"""

# importing libraries
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense

import warnings
warnings.filterwarnings('ignore')

# load json and create model
json_file = open('/content/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("/content/model.h5")

loaded_model.compile(loss='mean_squared_error', optimizer='adam')

# Unseen dataset
df = pd.read_csv('/content/NFLX.csv')

X_feat = df.iloc[:,1:5]

# Function to split and reshape X and y variables
def lstm_split (data, n_steps) :
  X, y = [], []
  for i in range(len(data)-n_steps+1):
    X.append(data[i:i+n_steps,:-1]) 
    y.append(data[i+n_steps-1,-1])
  return np.array(X), np.array (y)

X1, y1 = lstm_split(X_feat.values, n_steps=2)

preds = loaded_model.predict(X1, verbose=0)

print(pd.DataFrame(preds,columns=['Close']))

