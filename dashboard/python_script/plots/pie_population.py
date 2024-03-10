import os

import django
import pandas as pd
import plotly.express as px
from plotly.offline import plot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from dashboard.models import CovidData


def get_pie_population_plot(selected_countries, population):
    if isinstance(selected_countries, list):
        covid_data_objects = CovidData.objects.filter(
            Country__in=selected_countries)
    else:
        covid_data_objects = CovidData.objects.filter(
            Country=selected_countries)

    covid_data = pd.DataFrame(covid_data_objects.values('Confirmed'))
    total_confirmed = covid_data.max().iloc[0]

    fig = px.pie(values=[total_confirmed, population],
                 names=['Infected', 'Population'],
                 title='Population / Infected')
    fig.update_layout(title_x=0.5)

    config = {'displayModeBar': False}
    plot_div = plot(fig, config=config, output_type='div',
                    include_plotlyjs=False)
    return plot_div


if __name__ == '__main__':
    pass
