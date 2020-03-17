#imports for script
import pandas as pd
import geopandas as gpd
#Descartes are needed to plot polygons for maps
import descartes
from matplotlib import pyplot as plt
from matplotlib import cm
#from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import datetime

def main():
    #load todays date
    today = get_actual_time()

    #Define location of shape file
    shape_file = 'data/20200304/pandemic_germany.shp'

    #Define location of shape_file_state
    state_shape_file = 'vg2500_geo84/vg2500_bld.shp'

    #Read shape files
    germany, states = read_gdps(shape_file,state_shape_file)

    #Assign german states to gpd
    #germany = assign_state(germany, pd.read_csv('states_file.csv', sep=';'))

    #Create Cmap where value zero is 'white'
    cmap = create_cmap('tab20c', 120)

    #Create Pandemic Map
    print_map(germany, states, cmap, today)

def get_actual_time():
    return datetime.datetime.now()

def create_cmap(cmap, units):
    cmap = cm.get_cmap(cmap, units)
    cmap.colors[0] = [0,0,0,0]
    return cmap

def read_gdps(shape_file, state_shape_file):

    gdf = gpd.read_file(shape_file)
    gdf_state = gpd.read_file(state_shape_file)

    return gdf, gdf_state

def save_gdp(gdf, timeofday):

    gdf.to_file('data/202003{day}_{timeofday}/pandemic_germany.shp'.format(day=today.day, timeofday=timeofday))
    print("Save at 'data/202003{day}_{timeofday}'.format(day=today.day, timeofday=timeofday)")

def print_map(gdf_kreise, gdf_bdl, cmap, today):

    ax = gdf_kreise.plot(column='CORONA_AMT', legend=True, cmap=cmap, edgecolor='grey')
    gdf_bdl.plot(ax=ax, edgecolor='black', facecolor='None')

    #Set Title of Plot
    plt.title('Cases of COVID-19 in Germany {year}-{month}-{day}'.format(year=today.year, month=today.month, day=today.day))
    plt.show()

def assign_state(gpd, df):

    gpd['Bundesland'] = 'Empty'

    for df_index, df_row in df.iterrows():
        for gpd_index, gpd_row in gpd.iterrows():
            if df_row.Kreis == gpd_row.Kreis:
                #gpd_row.Bundesland = df_row.Bundesland
                gpd.at[gpd_index, 'Bundesland'] = df_row.Bundesland
    print(gpd[gpd['Bundesland']=='Baden-Württemberg'])
    return gpd

if __name__ == '__main__':
    main()