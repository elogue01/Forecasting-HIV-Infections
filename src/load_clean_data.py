import pandas as pd
import numpy as np

def load_amfar_data():
    '''
    This function loads and cleans the amfar data.  This amfar data was downloaded
    from http://opioid.amfar.org/ as a zipped tsv file and unzipped locally.

    INPUT: None
    OUTPUT: Cleaned and reshaped dataframe containing
    '''
    #load Amfar opioid and HIV data
    opiod_df = pd.read_table('data/tmp/countydata.tsv',header=0)
    opiod_df['county_code'] = opiod_df.STATEFP*1000 + opiod_df.COUNTYFP # build a county code column
    opiod_df['county_code'] = opiod_df.county_code.astype(int)

    #make changes to the amfar dataframe
    #convert from long to wide format
    opiod_df_wide = opiod_df.pivot_table(values='VALUE', index=['county_code',
                                                                'COUNTY',
                                                                'STATEABBREVIATION',
                                                                'YEAR'], columns='INDICATOR').reset_index()
    opiod_df_wide.drop(['CDC_consult', 'vulnerable_rank'], axis=1, inplace=True) # drop unnecessary columns
    opiod_df_wide = opiod_df_wide[opiod_df_wide.YEAR >= 2008] # subset for years that have hiv data
    opiod_df_wide[['HIVdiagnoses',
                   'HIVincidence',
                   'HIVprevalence',
                   'HIVprevalence',
                   'PLHIV',
                   'drugdeathrate',
                   'drugdeaths']] = opiod_df_wide[['HIVdiagnoses',
                                                   'HIVincidence',
                                                   'HIVprevalence',
                                                   'HIVprevalence',
                                                   'PLHIV',
                                                   'drugdeathrate',
                                                   'drugdeaths']].fillna(0) #fill NaNs for suppressed data with zeroes
    return opiod_df_wide

def subset_amfar_df(df, year):
    '''
    This function will subset the given dataframe to the specified year.
    INPUT:  df - A pandas dataframe containing a 'YEAR' column for subsetting
            year - INT between 2008 and 2015
    OUTPUT: subsetted pandas dataframe
    '''
    #subset data to specified year
    sub_df = df[df.YEAR == year].copy()

    #drop columns having no 2015 data
    sub_df.drop(['num_SSPs',
                    'bup_phys',
                    'drugdep',
                    'pctunmetneed',
                    'nonmedpain'], axis=1, inplace=True)

    return sub_df

def extract_single_year_data(df):
    '''
    This function extracts all single year data from the amfar opiod dataframe
    and returns dataframe with these single year features.
    INPUT: df - pandas dataframe (unsubsetted amfar dataframe)
    OUTPUT: pandas dataframe with only single year amfar data
    '''
    #subset opioid related data from one year only
    opiod_df_wide_16 = df[df.YEAR == 2016].copy()
    opiod_df_wide_17 = df[df.YEAR == 2017].copy()
    #number of needle exchange programs
    df_num_SSP = opiod_df_wide_17[['num_SSPs', 'county_code']].copy()

    #number of doctors licensed to rx Buprenorphine
    df_bup_phys = opiod_df_wide_17[['bup_phys', 'county_code']].copy()

    #percent with drug dependency
    df_drugdep = opiod_df_wide_16[['drugdep', 'county_code']].copy()

    #percent unmet drug treatment need
    df_pctunmetneed = opiod_df_wide_16[['pctunmetneed', 'county_code']].copy()

    #percent taken pain meds for nonmedical use
    df_nonmedpain = opiod_df_wide_16[['nonmedpain', 'county_code']].copy()

    #merge all these data into one df
    merge_df = df_num_SSP.merge(df_bup_phys, on='county_code')
    for dataframe in [df_drugdep, df_pctunmetneed, df_nonmedpain]:
        merge_df = merge_df.merge(dataframe, on='county_code')

    return merge_df

def make_amfar_df(subset_year):
    '''
    Loads amfar data subsetted by year together with data for which there is only
    data for a single year.
    INPUT: subset_year - INT between 2008 and 2015
    OUTPUT: pandas dataframe
    '''
    df = load_amfar_data() #load cleaned/reshaped amfar dataframe
    subset_year_df = subset_amfar_df(df, subset_year) #subset year of interest
    single_year_df = extract_single_year_data(df) #extract single year data
    merge_df = subset_year_df.merge(single_year_df, on='county_code') #merge subset and single year

    return merge_df

def make_acs_df():
    '''
    This function loads and cleans the american community survey data.  These
    data were downloaded from https://factfinder.census.gov/ as a zipped csv files
    and unzipped/renamed locally.
    '''
    #Load American Community Survey 5yr data from 2014
    #unemplyment data
    df_employment = pd.read_csv("data/ACS_14_5YR_employment/ACS_14_5YR_S2301_with_ann.csv",
                                encoding = "ISO-8859-1", skiprows=1)
    df_employment = df_employment[['Id2',
                                   'Unemployment rate; Estimate; Population 16 years and over']]
    df_employment.columns = ['county_code', 'unemployment_rate'] #rename columns

    #poverty data
    df_poverty = pd.read_csv("data/ACS_14_5YR_poverty/ACS_14_5YR_S1701_with_ann.csv",
                            encoding = "ISO-8859-1", skiprows=1)
    df_poverty = df_poverty[['Id2',
                             'Percent below poverty level; Estimate; Population for whom poverty status is determined']]
    df_poverty.columns = ['county_code', 'poverty_rate'] #rename columns

    #income data
    df_income = pd.read_csv("data/ACS_14_5YR_income/ACS_14_5YR_S1901_with_ann.csv", encoding = "ISO-8859-1", skiprows=1)
    df_income = df_income[['Id2', 'Households; Estimate; Total']]
    df_income.columns = ['county_code', 'household_income'] #rename columns

    #demographic data
    df_demo = pd.read_csv("data/ACS_14_5YR_age_sex_race/ACS_14_5YR_DP05_with_ann.csv",
                         encoding = "ISO-8859-1", skiprows=1)
    df_demo = df_demo[['Id2',
                       'Percent; SEX AND AGE - Total population - Male',
                       'Percent; SEX AND AGE - 20 to 24 years',
                       'Percent; SEX AND AGE - 25 to 34 years',
                       'Percent; SEX AND AGE - 35 to 44 years',
                       'Percent; RACE - Race alone or in combination with one or more other races - Total population - White',
                       'Percent; RACE - Race alone or in combination with one or more other races - Total population - Black or African American',
                       'Percent; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race)']]
    df_demo.columns = ['county_code',
                       'perc_male',
                       'perc_20_24',
                       'perc_25_34',
                       'perc_35_44',
                       'perc_white',
                       'perc_black',
                       'perc_hisp'] #rename columns
    # new column for percentage of 20-44 year olds
    df_demo['perc_20_44'] = df_demo.perc_20_24 + df_demo.perc_25_34 + df_demo.perc_35_44
    df_demo.drop(['perc_20_24',
                  'perc_25_34',
                  'perc_35_44'], axis=1, inplace=True) #drop old columns
    #merge these data
    merge_df = df_employment.merge(df_poverty, on='county_code')
    for dataframe in [df_income, df_demo]:
        merge_df = merge_df.merge(dataframe, on='county_code')

    return merge_df

def load_msm_df():
    '''
    This function loads and cleans the Emorycamp men who have sex with men (MSM)
    estimates.  These data were downloaded from
    http://emorycamp.org/item.php?i=48 as a csv file.
    '''

    #load Men who have sex with men (MSM) estimate data
    msm_df = pd.read_csv("data/US MSM Estimates Data 2013.csv") #load the data
    # build a county code column
    msm_df['county_code'] = msm_df.STATEFP*1000 + msm_df.COUNTYFP
    msm_df['county_code'] = msm_df.county_code.astype(int)
    # build a %MSM within last 12 months and last 5 years columns
    msm_df['%msm12month'] = 100 * (msm_df.MSM12MTH / msm_df.ADULTMEN)
    msm_df['%msm5yr'] = 100 * (msm_df.MSM5YEAR / msm_df.ADULTMEN)
    msm_df.drop(['REGCODE',
                 'DIVCODE',
                 'STATEFP',
                 'COUNTYFP',
                 'CSACODE',
                 'CBSACODE',
                 'METDCODE',
                 'METMICSA',
                 'CENTOUTL'], axis=1, inplace=True) #drop all unneeded columns
    return msm_df

def load_all_data(year):
    '''
    Loads amfar, acs and msm data subsetting amfar data by year and delivers a
    final merged dataframe containing all data
    INPUT: subset_year - INT between 2008 and 2015
    OUTPUT: pandas dataframe  (one dataframe to rule them all!)
    '''
    # load the three dataframes
    amfar_df = make_amfar_df(year)
    acs_df = make_acs_df()
    msm_df = load_msm_df()

    #merge into one final dataframe
    final_df = amfar_df.merge(acs_df, on='county_code')
    final_df = final_df.merge(msm_df, on='county_code')

    return final_df




if __name__ == '__main__':
    amfar_df = load_amfar_data()
    print(amfar_df.shape)
    amfar_2015_df = subset_amfar_df(amfar_df, 2015)
    print(amfar_2015_df.shape)
    amfar_single = extract_single_year_data(amfar_df)
    print(amfar_single.shape)
    final_amfar_df = make_amfar_df(2015)
    print(final_amfar_df.shape)
    acs_df = make_acs_df()
    print(acs_df.shape)
    msm_df = load_msm_df()
    print(msm_df.shape)
    df = load_all_data(2015)
    print(df.shape)
    print(df.head())
