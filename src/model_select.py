import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV, LassoLarsCV, LassoLarsIC
import load_clean_data as load



def score_model(data, model_list, features, target_col):
    '''
    This scores a list of models for their criterion score (AIC or BIC)
    INPUT: data - pandas dataframe
           model_list - list of instanciated models
           features - list of strings that match column names
           target_col - string that matches the target column name

    OUTPUT: List containing feature names, and scores for each model
    '''

    # define and scale the feature matrix
    X = data[features].values
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    # define the target vector
    y = df_no_zero_outlier[target_col].values

    # iterate the list of models to populate the score vector
    score = [features]
    for model in model_list:
        model.fit(X, y)
        score.append(round(model.criterion_.min(), 2))

    return score


def model_selection(data, features_list, target_col):
    '''
    This model instantiates a number of lasso regression models with different
    features and returns the BIC and AIC scores for each model.
    INPUT: data - pandas dataframe
           features_list  - a list of a list of strings that match column names
           target_col - string that matches the target column name
    OUTPUT: pandas dataframe containing features used with their BIC/AIC scores
    '''

    # instantiate the models for bic and aic scoring
    model_bic = LassoLarsIC(criterion='bic')
    model_aic = LassoLarsIC(criterion='aic')
    model_lst = [model_bic, model_aic]

    # iterate the features list to populate the scores list
    score_lst = []
    for features in features_list:
        score = score_model(data, model_lst, features, target_col)
        score_lst.append(score)

    # turn scores list into a pandas df
    score_df = pd.DataFrame(score_lst, columns=['Features', "BIC", 'AIC'])
    score_df['Features'] = score_df['Features'].apply(lambda x: ' + '.join(x))
    score_df['num_features'] = [len(x) for x in score_df.Features]

    return score_df


if __name__ == '__main__':
    df = load.load_all_data(2015)
    df_no_zero_outlier = df[((df.HIVincidence > 0) & (df.HIVincidence < 130))]
    features_list = [['HIVprevalence'], ['HIVprevalence', 'perc_black'], ['HIVprevalence', 'perc_white'],
                  ['HIVprevalence', 'perc_black', 'perc_white'],
                  ['HIVprevalence', 'perc_black', 'pctunins'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'poverty_rate'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'poverty_rate', 'pctunmetneed'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'pctunmetneed'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'drugdep'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'nonmedpain'],
                  ['HIVprevalence','perc_black','pctunins','poverty_rate','drugdep','nonmedpain'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm12month'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm5yr'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm5yr', 'perc_20_44'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm5yr', 'perc_20_44', 'Med_MH_fac'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm5yr', 'perc_20_44', 'Med_MH_fac', 'Med_SMAT_fac'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm5yr', 'perc_20_44', 'Med_MH_fac', 'Med_SMAT_fac', 'mme_percap'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm5yr', 'perc_20_44', 'Med_MH_fac', 'Med_SMAT_fac', 'mme_percap', 'partD30dayrxrate'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', '%msm5yr', 'perc_20_44', 'Med_MH_fac', 'Med_SMAT_fac', 'mme_percap', 'partD30dayrxrate', 'bup_phys'],
                  ['HIVprevalence', 'perc_black', 'pctunins', 'log_household_income', 'perc_20_44', 'mme_percap']]

    df = model_selection(df_no_zero_outlier, features_list, target_col='HIVincidence')

    print(df)
