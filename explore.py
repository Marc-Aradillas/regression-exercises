import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from scipy import stats

# custom imports
import wrangle
import prepare



# ------------------------------- VAR PAIRS FUNCTION --------------------------------------
# defined function for plotting all variable pairs.
def plot_variable_pairs(df):
    """
    This function plots all of the pairwise relationships along with the regression line for each pair.

    Args:
      df: The dataframe containing the data.

    Returns:
      None.
    """
    sns.set(style="ticks")
    
    # Created a pairplot with regression lines
    sns.pairplot(df, kind="reg", diag_kind="kde", corner=True)
    plt.show()







# ------------------------------- CAT|CONT VARS FUNCTION --------------------------------------
def plot_categorical_and_continuous_vars(df, continuous_var, categorical_var):
    """
    This function outputs three different plots for visualizing a categorical variable and a continuous variable.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        continuous_var (str): The name of the column that holds the continuous feature.
        categorical_var (str): The name of the column that holds the categorical feature.

    Returns:
        None.
    """

    # Created subplots with 1 row and 3 columns
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Box plot of the continuous variable for each category of the categorical variable
    sns.boxplot(x=categorical_var, y=continuous_var, data=df, ax=axes[0], bins=10)
    axes[0].set_title('Box plot of {} for each category of {}'.format(continuous_var, categorical_var))

    # Violin plot of the continuous variable for each category of the categorical variable
    sns.scatterplot(x=categorical_var, y=continuous_var, data=df, ax=axes[1], bins=10)
    axes[1].set_title('Scatter plot of {} for each category of {}'.format(continuous_var, categorical_var))

    # Histogram of the continuous variable for each category of the categorical variable
    for cat in df[categorical_var].unique():
        sns.histplot(df[df[categorical_var] == cat][continuous_var], ax=axes[2], label=cat, kde=True, bins=10)
    axes[2].set_title('Histogram of {} for each category of {}'.format(continuous_var, categorical_var))
    axes[2].legend(title=categorical_var)

    plt.tight_layout()
    plt.show()
'''
Example:

plot_categorical_and_continuous_vars(your_dataframe, "continuous_column", "categorical_column")
'''








# __________________________________________STATS test functions _________________________________________

# move this


def pearsonr(x, y, a=0.05):
    
    r, p = stats.pearsonr(x, y)
    
    if p < a:
        
        print("Reject the null hypothesis\n")

        print(f"There is a significant linear correlation between {x.name} and {y.name}. {p}\n")
        
    else:
        
        print("Fail to reject the null hypothesis\n")
        
        print(f"There is no significant linear correlation between {x.name} and {y.name}. {p}\n")
    
    return r, p








# __________________________________________

def spearmanr(x, y, alpha=0.05):
    
    rho, p = stats.spearmanr(x, y)
    
    if p < alpha:
        
        print("Reject the null hypothesis\n")

        print(f"There is a significant monotonic correlation between {x.name} and {y.name}. {p}\n")
        
    else:
        
        print("Fail to reject the null hypothesis")

        print(f"There is no significant monotonic correlation between {x.name} and {y.name}. {p}\n")

    return rho, p