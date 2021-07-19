import pandas as pd
import json
import altair as alt
import numpy as np
from shapely import wkt
import matplotlib.pyplot as plt

def stacked_chart():
    df = pd.read_json("http://localhost:8000/timeline")
    df = df.drop(["primera_dosis", "segunda_dosis", "acum_primera_dosis", "acum_segunda_dosis"], axis=1)
    df.columns = ["Fecha", "Primera dosis", "Ambas dosis"]
    long_df = df.melt('Fecha', var_name='dosis', value_name='cantidad')

    chart = alt.Chart(long_df).mark_area(color="blue", opacity=0.5).encode(
        x="Fecha:T",
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

def barchart():
    df = pd.read_json("http://localhost:8000/provinces/vaccines")
    df = df.drop(["jurisdiccion_codigo_indec", "primera_dosis", "segunda_dosis", "total_dosis", "poblacion"], axis=1)
    df.columns = ["Provincia", "1° Dosis", "Ambas dosis"]
    df["1° Dosis"] -= df["Ambas dosis"]
    long_df = df.melt('Provincia', var_name='Dosis', value_name='Población vacunada (%)')
    colors = ['#98B9AB', '#3E6990']
    chart = alt.Chart(long_df).mark_bar().encode(
        x='Población vacunada (%)',
        y = alt.Y('Provincia', sort='-x'),
        color=alt.Color('Dosis', scale=alt.Scale(range=colors))
    )
    chart.show()



def main():
    stacked_chart()
    barchart()

if __name__ == "__main__":
    alt.renderers.enable('html')
    main()
