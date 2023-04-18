import pandas as pd
from sklearn.preprocessing import LabelEncoder
data = pd.read_csv('E:/ASE/ASE-Project/etc/data/coc10000.csv')

change_Cols = [col for col in data.columns if col.strip()[0].islower() and data[col].dtypes == 'O']
print(data.head())

le = LabelEncoder()
for sym in change_Cols:
  temp_column = le.fit_transform(data[sym])
  data[sym] = temp_column.copy()
     
data.head()
print(change_Cols)

data.to_csv('E:/ASE/ASE-Project/etc/data/mod_coc10000.csv', index=False)
