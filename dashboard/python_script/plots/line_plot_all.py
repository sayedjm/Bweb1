import os

import django
import pandas as pd
import plotly.express as px
from plotly.offline import plot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from dashboard.models import CovidData


def get_all_lines_plot():
    covid_data_df = pd.DataFrame(list(CovidData.objects.values('Country', 'Confirmed', 'ObservationDate')))
    covid_data_df['Date'] = pd.to_datetime(covid_data_df['ObservationDate'])
    grouped_df = covid_data_df.groupby(['Country', 'Date'])['Confirmed'].sum().reset_index()
    fig = px.line(grouped_df, x='Date', y='Confirmed', color='Country', template='plotly_white')
    config = {'displayModeBar': False}
    plot_div = plot(fig, config=config, output_type='div', include_plotlyjs=False)
    return plot_div


if __name__ == '__main__':
    pass
