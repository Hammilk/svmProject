#start

import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer

relative_path = os.path.join('gas_sensor_data.csv')
df = pd.read_csv(relative_path)
imp = SimpleImputer(missing_values=np.nan, strategy='mean')
imputed_data = imp.fit_transform(df)
imputed_df = pd.Dataframe(imputed_data, columns = df.columns)


