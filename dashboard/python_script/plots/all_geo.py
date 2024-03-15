import os

import django
import pandas as pd
import plotly.express as px
from plotly.offline import plot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from dashboard.models import CovidData
from dashboard.python_script.data.convert_to_iso_alpha import convert_to_iso_alpha


def get_all_geo_plot():
    covid_data_df = pd.DataFrame(list(CovidData.objects.values('Country', 'Confirmed', 'ISO3166_CountryCode')))

    max_values = covid_data_df.groupby("Country").agg({'Confirmed': 'max', 'ISO3166_CountryCode': 'first'}).reset_index()
    max_values['Iso_alpha'] = max_values['ISO3166_CountryCode'].apply(convert_to_iso_alpha)

    fig = px.scatter_geo(max_values, locations="Iso_alpha", color="Country",
                         hover_name="Country", size="Confirmed",
                         projection="orthographic")
    fig.update_layout(showlegend=False, title_x=0.5)
    config = {'displayModeBar': False}

    plot_div = plot(fig, config=config, output_type='div',
                    include_plotlyjs=False)
    return plot_div


if __name__ == '__main__':
    pass
