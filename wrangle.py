import os
import pandas as pd
import numpy as np



# ----------------------ACQUIRE FUNCTION---------------------------------
def get_z_data():
    '''
    Read student_grades into a pandas DataFrame from mySQL,
    drop student_id column, replace whitespaces with NaN values,
    drop any rows with Null values, convert all columns to int64,
    return cleaned student grades DataFrame.
    '''

    # Acquire data

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