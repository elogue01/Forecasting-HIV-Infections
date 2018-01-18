import pandas as pd
import numpy as np

def load_amfar_data():
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

def subset_amfar_df(year):




if __name__ == '__main__':
    amfar_df = load_amfar_data()
    print(amfar_df.shape)
