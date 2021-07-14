import altair as alt

# load a simple dataset as a pandas DataFrame
from vega_datasets import data
alt.renderers.enable('mimetype')
cars = data.cars()

chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()

chart.show()