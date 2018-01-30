import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from pymc3 import Model, sample, Normal, HalfCauchy, Uniform, traceplot, summary, forestplot
from pymc3.glm import GLM
import load_clean_data as load


def make_levels(df, level_feature):
    df_levels = df[level_feature].unique()
    n_levels = len(df_levels)
    level_lookup = dict(zip(df_levels, range(len(df_levels))))
    level = df['level_code'] = df[level_feature].replace(level_lookup).values

    return df_levels, n_levels, level

def prep_data(df, var_cols, target_col):
    X = df_no_zero_outlier[var_cols].values


    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    y = df_no_zero_outlier[target_col].values

    return X, y

def pooled_model(X,y):
    data = dict(x1=X[:,0], x2=X[:,1], x3=X[:,2], x4=X[:,3], y=y)
    with Model() as pooled_model:
    # specify glm and pass in data. The resulting linear model, its likelihood and
    # and all its parameters are automatically added to our model.
    GLM.from_formula('y ~ 1 + x1 + x2 + x3 +x4', data)
    # draw 3000 posterior samples using NUTS sampling
    trace = sample(1000, n_init=50000, tune=1000, njobs=1)

    return pooled_model, trace

def unpooled_model(X, y, level, n_levels):
    with Model() as unpooled_model:

    intercept = Normal('intercept', 0, sd=1e5, shape=n_levels)
    beta1 = Normal('beta1', 0, sd=1e5)
    beta2 = Normal('beta2', 0, sd=1e5)
    beta3 = Normal('beta3', 0, sd=1e5)
    beta4 = Normal('beta4', 0, sd=1e5)

    sigma = HalfCauchy('sigma', 5)

    theta = intercept[level] + beta1 * X[:,0] + beta2 * X[:,1] + beta3 * X[:,2] + beta4 * X[:,3]
    y = Normal('y', theta, sd=sigma, observed=y)

    with unpooled_model:
    unpooled_trace = sample(1000, n_init=50000, tune=1000)

    return unpooled_model, unpooled_trace


def multi_model(X, y, level, n_levels):

    with Model() as multi_model:
    #set intercept hyper priors
    mu_intercept = Normal('mu_intercep', mu=0., sd=1e5)
    sigma_intercept = HalfCauchy('sigma_intercep', 5)

    #set beta1 hyper priors
    mu_beta1 = Normal('mu_beta1', mu=0., sd=1e5)
    sigma_beta1 = HalfCauchy('sigma_beta1', 5)

    #set beta2 hyper priors
    mu_beta2 = Normal('mu_beta2', mu=0., sd=1e5)
    sigma_beta2 = HalfCauchy('sigma_beta2', 5)

    #set beta3 hyper priors
    mu_beta3 = Normal('mu_beta3', mu=0., sd=1e5)
    sigma_beta3 = HalfCauchy('sigma_beta3', 5)

    #set beta4 hyper priors
    mu_beta4 = Normal('mu_beta4', mu=0., sd=1e5)
    sigma_beta4 = HalfCauchy('sigma_beta4', 5)

    intercept = Normal('intercept', mu=mu_intercept, sd=sigma_intercept, shape=n_levels)
    beta1 = Normal('beta1', mu=mu_beta1, sd=sigma_beta1, shape=n_levels)
    beta2 = Normal('beta2', mu=mu_beta2, sd=sigma_beta2, shape=n_levels)
    beta3 = Normal('beta3', mu=mu_beta3, sd=sigma_beta3, shape=n_levels)
    beta4 = Normal('beta4', mu=mu_beta3, sd=sigma_beta4, shape=n_levels)

    sigma = HalfCauchy('sigma', 5)

    HIV_like = intercept[level] + beta1[level] * X[:,0] + beta2[level] * X[:,1] + beta3[level] * X[:,2] + beta4[level] * X[:,3]
    y = Normal('y', HIV_like, sd=sigma, observed=y)

    with multi_model:
    multi_trace = sample(1000, n_init=150000, tune=50000)


    return multi_model, multi_trace


def score_model(model, trace):

    waic_score = stats.waic(model=model, trace=trace)
    loo_score = stats.loo(model=pooled_model_X, trace=pooled_X_trace)

    print('WAIC for this model is {} ({})'.format(round(waic_score[0], 2),
                                                round(waic_score[1], 2)))

    print('LOO for this model is {} ({})'.format(round(loo_score[0], 2),
                                                round(loo_score[1], 2)))

if __name__ == '__main__':
    df = load.load_all_data(2015)
    df_no_zero_outlier = df[((df.HIVincidence > 0) & (df.HIVincidence < 130))].copy()
    us_states, n_states, state = make_levels(df_no_zero_outlier, 'STATEABBREVIATION')
    print(us_states, n_states, state)
