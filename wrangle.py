import os
import pandas as pd
import numpy as np

 # Acquire data.
# ----------------------ACQUIRE FUNCTION---------------------------------
def get_z_data():
    
    filename = 'sfr_2017.csv'

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

        df.to_csv(filename, index=False)

        return df 


# Prep data.
# ---------------------------CLEAN FUNCTION----------------------------
def clean_z_data():
    
    df = get_z_data()
    
    # Drop rows with missing values in any column
    df = df.dropna()

    # Convert selected columns to integer type
    int_columns = ['fips', 'yearbuilt', 'taxvaluedollarcnt', 'calculatedfinishedsquarefeet']
    df[int_columns] = df[int_columns].astype(int)

    # Remove rows where bathroomcnt or bedroomcnt is 0.0
    df = df[(df.bathroomcnt != 0.0) & (df.bedroomcnt != 0.0)]

    return df


# wrapping Acquire and Prep functions into one.
# ---------------------------- WRANGLE ZILLOW -------------------------------------
def wrangle_zillow():

    df = get_z_data()

    df = clean_z_data()

    return df