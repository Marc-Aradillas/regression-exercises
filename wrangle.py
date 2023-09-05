import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from env import get_connection




# Constants
filename = 'zillow_data.csv'

# Acquire data.
# ----------------------ACQUIRE FUNCTION---------------------------------
def acquire_zillow():

    if os.path.isfile(filename):
        
        return pd.read_csv(filename)
        
    else: 

        query = '''
                SELECT 
                    bedroomcnt,
                    bathroomcnt,
                    calculatedfinishedsquarefeet,
                    taxvaluedollarcnt,
                    yearbuilt,
                    taxamount,
                    fips
                FROM 
                    properties_2017
                WHERE 
                    propertylandusetypeid = 261; -- 'Single Family Residential'
                '''

        url = get_connection('zillow')
                
        df = pd.read_sql(query, url)

        # # save to csv
        # df.to_csv(filename,index=False)

        return df 


# Prep data.
# ---------------------------CLEAN FUNCTION----------------------------
def clean_zillow(df):

    """
    Cleans the Zillow data.
    
    Args:
    - df (DataFrame): Raw Zillow data.
    
    Returns:
    - cleaned_df (DataFrame): Cleaned Zillow data.
    """
    
    # Drop rows with missing values in any column
    df = df.dropna()

    # Rename columns
    df = df.rename(columns={'bedroomcnt': 'bedrooms', 'bathroomcnt': 'bathrooms', 'calculatedfinishedsquarefeet': 'area', 'taxvaluedollarcnt': 'tax_value', 'yearbuilt': 'year_built', 'taxamount': 'tax_amount'})

    # Convert selected columns to integer type
    int_columns = ['fips', 'year_built', 'tax_value', 'area', 'bedrooms']
    df[int_columns] = df[int_columns].astype(int)

    # Remove rows where bathroomcnt or bedroomcnt is 0.0
    # df = df[(df.bedrooms != 0.0) & (df.bathrooms != 0.0)]

    # initial_df = {'county': ['LOS ANGELES', 'ORANGE', 'VENTURA'], 'fips' : [6037, 6059, 6111]}
    
    # df1=pd.DataFrame(initial_df)
    
    # df=df1.merge(df)
    
    # df.set_index(df['fips'], inplace=True)
    
    return df

# wrapping Acquire and Prep functions into one.
# ---------------------------- WRANGLE ZILLOW -------------------------------------
def wrangle_zillow():
    """
    Wrangles Zillow data by acquiring and cleaning it.
    
    Returns:
    - df (DataFrame): Wrangled Zillow data.
    """
    # Acquire data
    df = acquire_zillow()
    
    # Clean data
    df = clean_zillow(df)

    df.to_csv(filename, index=False)

    return df

# ------------------------ SPLIT FUNCTION -------------------------

def train_val_test(df, seed = 42):
    """
    splits cleaned df into train, validate, and split
    
    Returns:
    - train, validate, split subset of df (dataframe): Splitted Wrangles Zillow Data
    """
    
    train, val_test = train_test_split(df, train_size = 0.7,
                                       random_state = seed)
    
    val, test = train_test_split(val_test, train_size = 0.5,
                                 random_state = seed)
    
    return train, val, test