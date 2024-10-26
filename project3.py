import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
from sklearn import svm
from feature_engine.selection import DropCorrelatedFeatures
from sklearn.model_selection import GridSearchCV

relative_path = os.path.join('gas_sensor_data.csv')
df = pd.read_csv(relative_path)

#Split dataframe into X, Y
y = pd.DataFrame(df['gas_label'])
y_columns = y.columns
x_temp = df.drop(['gas_label'], axis = 1)
x = x_temp.drop(['Batch ID'], axis = 1)
x_columns = x.columns


#Smote class resampling
y_np = np.array(y)
y_np = y_np.ravel()
x_np = np.array(x)

#Handle Missing Values
imp = SimpleImputer(missing_values=np.nan, strategy='mean')
x_imputed = imp.fit_transform(x_np)



#Label Encode Y Values
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_np)

smote = SMOTE(random_state=42)
x_resampled, y_resampled = smote.fit_resample(x_np, y_encoded)

#Split
x_train, x_test, y_train, y_test = train_test_split(x_resampled, y_resampled, test_size=.33, random_state=42)

#Standardize
scalar = StandardScaler()
x_train_std = scalar.fit_transform(x_train)
x_test_std = scalar.fit_transform(x_test)

#Create correlation matrix
df_corr = pd.DataFrame(x_train_std, columns = x_columns)
df_test = pd.DataFrame(x_test_std, columns = x_columns)
drop_correlated = DropCorrelatedFeatures(threshold=0.7)

drop_correlated.fit(df_corr)
final_df = drop_correlated.transform(df_corr)
final_test = drop_correlated.transform(df_test)

x_train_model = np.array(final_df)
x_test_model = np.array(final_test)

param_grid = {
        'C': [0.01, 0.1, 1, 10, 100],
        'max_iter': [-1, 100, 1000, 5000],
        'class_weight': ['balanced', None],
}

"""
grid_search = GridSearchCV(svm.SVC(kernel='linear'), param_grid, cv=5)
grid_search.fit(x_train_std, y_train)
print("Best parameters:", grid_search.best_params_)

"""
#Linear SVM
linear_svm = svm.SVC(C=100, class_weight='balanced', kernel='linear', decision_function_shape='ovr')
linear_svm.fit(x_train_model, y_train)
y_pred = linear_svm.predict(x_test_model)

print(classification_report(y_test, y_pred))

"""
param_grid_rbf = {
        'C': [0.1, 1, 10, 100],
        'gamma': [.001, .01, .1, 1, 10]
}

grid_search = GridSearchCV(svm.SVC(kernel='rbf'), param_grid, cv=5, scoring='accuracy')
grid_search.fit(x_train_std, y_train)
print("Best parameters: ", grid_search.best_params_)

#RBF SVM
nonlinear_svm = svm.SVC(kernel='rbf', C=100, class_weight='balanced')
nonlinear_svm.fit(x_train_model, y_train)

y_pred_rbf = linear_svm.predict(x_test_model)

print(classification_report(y_test, y_pred_rbf))
"""






