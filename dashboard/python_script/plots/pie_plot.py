import os

import django
import pandas as pd
import plotly.express as px
from plotly.offline import plot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from dashboard.models import CovidData


def get_pie_plot(selected_country):
    if isinstance(selected_country, list):
        covid_data_objects = CovidData.objects.filter(Country__in=selected_country)
    else:
        covid_data_objects = CovidData.objects.filter(Country=selected_country)
    covid_data = pd.DataFrame(covid_data_objects.values('Confirmed', 'Recovered', 'Deaths'))
    total_values = covid_data.max()
    fig = px.pie(total_values,values=total_values.values, names=total_values.index, title=f'Distribution Confirmed, Recovered and Deaths')
    fig.update_layout(showlegend=False, title_x=0.5)
    config = {'displayModeBar': False}
    plot_div = plot(fig, config=config, output_type='div', include_plotlyjs=False)
    return plot_div


if __name__ == '__main__':
    pass
