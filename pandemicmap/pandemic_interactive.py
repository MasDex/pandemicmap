#-----------------------------------------#
#               Make Imports              #
#-----------------------------------------#

import json

from bokeh.io import show

from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)

from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh import palettes
from bokeh.plotting import figure

import geopandas as gpd
import pandas as pd

from datetime import date

# Define location of shape_file_state
state_shape_file = 'vg2500_geo84/vg2500_bld.shp'

def main():

    #Load RKI DataFrame
    df = pd.read_csv('data/rki_files/pandemic_data_clean_{today}.csv'.format(today=date.today().strftime("%Y%m%d")), sep=',')
    df.CONFIRMED_CORONA_AMT = df.CONFIRMED_CORONA_AMT.astype('int')

    #shape_file = 'data/20200304/pandemic_germany.shp'
    germany_states = gpd.read_file(state_shape_file)

    #Drop unnecessary columns
    germany_states = germany_states.drop(['RS_ALT', 'USE', 'RS'], axis=1)

    #Rename Columns of Shapefile
    germany_states.columns = ['STATE', 'SHAPE_LENG', 'SHAPE_AREA', 'geometry']

    #Merge DataFrame into GeoDataFrame
    germany_states = germany_states.merge(df, on='STATE')

    # Input GeoJSON source that contains features for plotting
    geosource = GeoJSONDataSource(geojson= germany_states.to_json())


    #Define color palettes
    #palette = brewer['RdYlGn'][11]
    palette =  palettes.Turbo256
    #palette = palette[::-1] #reverse order of colors so higher values have darker colors

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette=palette, low= 0, high= 1500)


    tick_labels = {'0':'0', '100':'100','200':'200', '300':'300', '400':'400', '500':'500',
    '600':'600', '700':'700','800':'800','900':'900','1000':'1000', '1200':'1200', '1300':'1300', '1400':'1400', '1500':'1500+'}

    #Create Colorbar
    color_bar = ColorBar(color_mapper= color_mapper,
                         label_standoff= 8,
                         width= 500, height= 20,
                         border_line_color = None,
                         location= (0,0),
                         orientation= 'horizontal',
                         major_label_overrides= tick_labels)

    #Create figure object
    p = figure(title='Pandermic Germany COVID-19',
               plot_height= 600, plot_width= 600,
               toolbar_location= 'below',
               tools= 'pan, wheel_zoom, box_zoom, reset')

    p.xgrid.grid_line_color= None
    p.ygrid.grid_line_color= None

    # Add patch renderer to figure.
    states = p.patches('xs','ys', source= geosource,
                       fill_color = {'field':'CONFIRMED_CORONA_AMT',
                                     'transform':color_mapper},
                       line_color = 'black',
                       line_width= .25,
                       fill_alpha= 1)

    # Create Hover Tool
    p.add_tools(HoverTool(renderers=[states],
                          tooltips=[('Bundesland', '@STATE'),
                                    ('Corona Fälle', '@CONFIRMED_CORONA_AMT'),
                                    ('Todesfälle', '@CONFIRMED_DEATHS')]))
    #Specify Layout
    p.add_layout(color_bar, 'below')

    show(p)





if __name__ == '__main__':
    main()