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


#-------------------------PREPARE MODULE------------------------------


# -----------------Train-Validate-Test-------------------------------
# function to subset data
def train_val_test(df, seed = 42):

    train, val_test = train_test_split(df, train_size=0.7, random_state=seed)
    val, test = train_test_split(val_test, train_size=0.5, random_state=seed)

    return train, val, test



# - - - - - - - - - - - Scale Data - - - - - - - - - - - - - - - -
# Define a function for scaling the data
def scale_data(train, val, test, scaler):
    
    # Fit the scaler on the training data
    scaler.fit(train[['tax_value']])
    
    # Transform the data for each split
    train['tax_value_scaled'] = scaler.transform(train[['tax_value']])
    val['tax_value_scaled'] = scaler.transform(val[['tax_value']])
    test['tax_value_scaled'] = scaler.transform(test[['tax_value']])
    
    return train, val, test



# --------------------Visualization function----------------------

def visualize_compare(scaled_col, df, original='tax_value'):
    plt.figure(figsize=(11, 7))

    plt.subplot(121)
    sns.histplot(data=df, x=original, bins=40)
    plt.title(f'Distribution original')
    
    plt.subplot(122)
    sns.histplot(data=df, x=scaled_col, bins=40)
    plt.title(f'Distribution scaled')

    plt.tight_layout()
    plt.show()


