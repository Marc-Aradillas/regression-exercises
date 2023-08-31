import os
import pandas as pd
import numpy as np
from env import get_connection

 # Acquire data.
# ----------------------ACQUIRE FUNCTION---------------------------------
def acquire_zillow():
    
    filename = 'zillow_data.csv'

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

        return df 


# Prep data.
# ---------------------------CLEAN FUNCTION----------------------------
def clean_zillow():
    
    df = acquire_zillow()
    
    # Drop rows with missing values in any column
    df = df.dropna()

    #rename cols
    df = df.rename(columns= {'bedroomcnt': 'bedrooms', 'bathroomcnt': 'bathrooms', 'calculatedfinishedsquarefeet' : 'area', 'taxvaluedollarcnt': 'tax_value', 'yearbuilt': 'year_built', 'taxamount': 'tax_amount'})

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

    # acquire data function
    df = acquire_zillow()
    
    # clean data function
    df = clean_zillow()

    # save to csv
    df.to_csv('zillow_data.csv',index=False)

    return df