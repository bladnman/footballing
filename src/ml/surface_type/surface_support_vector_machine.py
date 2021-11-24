#%%
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
import utils.game_utils as gu

import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, plot_confusion_matrix
from sklearn.svm import SVC

data_path = '../../../data'
nfld = gu.NFL_Data(data_path)
nfl_df = nfld.data()
year_df = gu.get_year(nfl_df, 2020)
df = year_df[['team','is_outdoors','win']]

print("We are using Support Vector Machines to determine if team and is_outdoors is a predictor")
print(df.head())

### Output results - helper
def print_results(model, X_test, y_test, y_pred):
  print('---------------')
  acc = accuracy_score(y_test, y_pred)
  print(f"Model Accuracy: {acc}")

  print('---------------')
  print("Confusion Matrix:")
  print(confusion_matrix(y_test, y_pred))

  print('---------------')
  print('Classification Report')
  print(classification_report(y_test, y_pred))
  # plot_confusion_matrix(model, X_test, y_test)


dum_df = pd.get_dummies(df)
X = dum_df.drop('win', axis=1)
y = dum_df['win']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)
model = SVC()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print('---------------')
print('USING Default SVC model')
print(f"{mean_absolute_error(y_test, y_pred):.3f} : Mean Absolute Error")
print(f"{np.sqrt(mean_squared_error(y_test, y_pred)):.3f} : Mean Error")

print_results(model, X_test, y_test, y_pred)

def get_model_from_search(X_train, y_train):
  param_grid = {'C':[0.001,0.01,0.1,0.5,1],
                'kernel':['linear','rbf','poly'],
                'gamma':['scale','auto'],
                'degree':[2,3,4],
                # 'epsilon':[0,0.01,0.1,0.5,1,2]
                }
  model = GridSearchCV(SVC(), param_grid=param_grid)
  model.fit(X_train, y_train)
  print(model.best_params_)
  # -> {'C': 1, 'degree': 2, 'gamma': 'scale', 'kernel': 'poly'}
  return model
def get_model_from_static(X_train, y_train):
  model = SVC(C=1, degree=2, gamma='scale', kernel='poly')
  model.fit(X_train, y_train)
  return model

# to calculate the best parameters
# model = get_model_from_search(X_train, y_train)

# to use previously calculated parameters
model = get_model_from_static(X_train, y_train)

# now predict
y_pred = model.predict(X_test)



print('---------------')
print('USING SEARCH Parameters')
print(f"{mean_absolute_error(y_test, y_pred):.3f} : Mean Absolute Error")
print(f"{np.sqrt(mean_squared_error(y_test, y_pred)):.3f} : Mean Error")

print_results(model, X_test, y_test, y_pred)


# %%
