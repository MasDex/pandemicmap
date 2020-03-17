import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime

def scrap_data():
    page = requests.get('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html')

    soup = BeautifulSoup(page.content, 'html.parser')

    #<table>
    table = soup.find('table')
    tbody = table.find('tbody')
    trow = tbody.find_all('tr')
    print(trow)

    data = []

    for row in trow:
        td = row.find_all('td')
        observation = []
        for column in td:

            print(column.renderContents().decode('utf-8').strip())
            observation.append(column.renderContents().decode('utf-8').strip())

        data.append(observation)

    return data


def store_data_as_df(data):
    today = datetime.now()

    df = pd.DataFrame(data)
    df.columns = ['Bundesland', 'Bestaetigte Faelle', 'Davon elektronisch uebermittelt', 'Schwerpunkt Gebiete']
    df.to_csv('data/rki_files/pandemic_data_raw_{date}.csv'.format(date=today.strftime("%Y%m%d_%H%M%S")), sep=';')

def main():
    data = scrap_data()
    store_data_as_df(data)

if __name__ == '__main__':
    main()
