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
    df = pd.read_json("http://localhost:8000/timeline")
    df = df.drop(["primera_dosis", "segunda_dosis", "acum_primera_dosis", "acum_segunda_dosis"], axis=1)
    df.columns = ["fecha", "Primera dosis", "Ambas dosis"]
    long_df = df.melt('fecha', var_name='dosis', value_name='cantidad')
    
    chart = alt.Chart(long_df).mark_area(color="blue", opacity=0.5).encode(
        x="fecha:T",
        y=alt.Y('cantidad:Q', title='Poblacion vacunada [%]', stack=None),
        color="dosis:N"
    ).properties(height=500)
    # chart2 = alt.Chart(long_df).mark_area(color="green",opacity=0.5).encode(
    #     x="fecha:T",
    #     y='porc_segunda_dosis:Q'
    # ).properties(height=150)
    # mixed = chart + chart2
    # mixed.show()
    chart.show()

def main():
    barchart()
    # choropleth_pais()

if __name__ == "__main__":
    alt.renderers.enable('html')
    # Mimetype se supone que hace una visualizacion desde el vscode, pero no me funciona
    # Por eso dejo la linea de arriba que hace renderer con html
    # alt.renderers.enable('mimetype')
    main()