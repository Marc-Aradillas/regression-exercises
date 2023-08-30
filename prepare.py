# imported libs for scaling
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, QuantileTransformer
from sklearn.model_selection import train_test_split

#custom import

import wrangle

# -----------------------------------PREPARE MODULE---------------------------------

def compare_data(scaled_col, df=(train, val, test), original='tax_value'):
    plt.figure(figsize=(11, 7))

    plt.subplot(121)
    sns.histplot(data=df, x=original, bins=40)
    plt.title(f'Distribution')
    
    plt.subplot(122)
    sns.histplot(data=df, x=scaled_col, bins=40)
    plt.title(f'Distribution')

    plt.tight_layout()
    plt.show()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - 

# Define a function for scaling the data
def scale_data(train, val, test, scaler):
    
    # Fit the scaler on the training data
    scaler.fit(train[['tax_value']])
    
    # Transform the data for each split
    train['tax_value_scaled'] = scaler.transform(train[['tax_value']])
    val['tax_value_scaled'] = scaler.transform(val[['tax_value']])
    test['tax_value_scaled'] = scaler.transform(test[['tax_value']])
    
    return train, val, test

# Load and wrangle data
df = wrangle.wrangle_zillow()

# Split the data
seed = 42

train, val_test = train_test_split(df, train_size=0.7, random_state=seed)
val, test = train_test_split(val_test, train_size=0.5, random_state=seed)

# Filter data
train = train[(train['tax_value'] < 3_000_000) & (train['tax_amount'] < 3_000_000)]
val = val[(val['tax_value'] < 3_000_000) & (val['tax_amount'] < 3_000_000)]
test = test[(test['tax_value'] < 3_000_000) & (test['tax_amount'] < 3_000_000)]

# different scalers
mms = MinMaxScaler()
ss = StandardScaler()
rs = RobustScaler()
qt = QuantileTransformer(output_distribution='normal', n_quantiles=10, random_state=seed)

# train, val, test = scale_data(train, val, test, mms)
train, val, test = scale_data(train, val, test, ss)
# train, val, test = scale_data(train, val, test, rs)
# train, val, test = scale_data(train, val, test, qt)

# Compare distributions for each scaled column
compare_data('tax_value_scaled', train)
compare_data('tax_value_scaled', val)
compare_data('tax_value_scaled', test)



