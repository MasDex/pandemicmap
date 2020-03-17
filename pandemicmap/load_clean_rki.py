import pandas as pd
import re
from datetime import date
import os, glob

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

today = date.today()
root_directory = 'pandemicmap/data/rki_files'

def load_df():

    #file_list = os.listdir('pandemicmap/data/rki_files/')

    list_of_files = glob.glob('pandemicmap/data/rki_files/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file = latest_file.split('/')[-1]

    file_path = 'pandemicmap/data/rki_files/{}'.format(latest_file)

    df = pd.read_csv(file_path, sep=';')

    return df

def clean_df(df):

    df = df.drop('Unnamed: 0', axis=1)
    df = df.drop(16, axis=0)

    for key, row in df.iterrows():
        if re.search(" ", df.loc[key, 'Bestaetigte Faelle']):
            data = split_bestaetigte_faelle(row['Bestaetigte Faelle'])
            data_elektronisch = split_bestaetigte_faelle(row['Davon elektronisch uebermittelt'])
            df.loc[key,'Bestaetigte Faelle'] = data[0]
            df.loc[key,'Davon elektronisch uebermittelt'] = data_elektronisch[0]
            df.loc[key,'Bestaetigte Todesfaelle'] = data[1]
            df.loc[key,'Bestaetigte Todesfaelle Elektronisch'] = data_elektronisch[1]
        else:
            df.loc[key,'Bestaetigte Todesfaelle'] = '0'
            df.loc[key,'Bestaetigte Todesfaelle Elektronisch'] = '0'

    df.columns = ['STATE', 'CONFIRMED_CORONA_AMT', 'REPORTED_DIGITAL_CORONA_AMT',
       'FOCUS_AREAS', 'CONFIRMED_DEATHS',
       'REPORTED_DIGITAL_DEATHS']

    return df




def split_bestaetigte_faelle(data):
        data = data.split()
        data[1] = data[1].replace('(','')
        data[1] = data[1].replace(')','')
        if re.search('.', data[0]):
            data[0] = data[0].replace('.','')
        return data


def main():
    df = load_df()
    df = clean_df(df)
    df.to_csv('pandemicmap/data/rki_files/pandemic_data_clean_{date}.csv'.format(date=today.strftime("%Y%m%d"), sep=';'))

if __name__ == '__main__':
    main()