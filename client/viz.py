import pandas as pd
import json
import altair as alt
import geopandas as gpd
import numpy as np
from shapely import wkt

import matplotlib.pyplot as plt
def choropleth_pais():
    # Choropleth pais
    # df = pd.DataFrame(
    # {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
    #  'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
    #  'Coordinates': ['POINT(-58.66 -34.58)', 'POINT(-47.91 -15.78)',
    #                  'POINT(-70.66 -33.45)', 'POINT(-74.08 4.60)',
    #                  'POINT(-66.86 10.48)']})
    # print(df)
    # exit()
    df = pd.read_json("http://localhost:8000/provinces/vaccines_geo")
    df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.plot()
    plt.show()
    choro_json = json.loads(gdf.to_json())
    choro_data = alt.Data(values=choro_json['features'])
    
    # Add Base Layer
    base = alt.Chart(choro_data, title = "asdf").mark_geoshape(
        stroke='black',
        strokeWidth=1
    ).encode(
    )
    base.show()

def barchart():
    df = pd.read_json("http://localhost:8000/provinces/vaccines")
    chart = alt.Chart(df).mark_bar().encode(
        y = alt.Y('total_dosis', sort='x'),
        x="jurisdiccion_nombre",
    ).properties(height=150)
    chart.show()

def main():
    # barchart()
    choropleth_pais()

if __name__ == "__main__":
    alt.renderers.enable('html')

    # alt.renderers.enable('mimetype')
    main()