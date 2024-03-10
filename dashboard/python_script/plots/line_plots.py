import os

import django
import pandas as pd
import plotly.express as px
from plotly.offline import plot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from dashboard.models import CovidData


def get_line_plot(selected_countries: list, observation: str) -> dict:
    all_data = []
    if type(selected_countries) == str:
        selected_countries = [selected_countries]
    for selected_country in selected_countries:
        covid_data = CovidData.objects.filter(Country=selected_country, **{
            f"{observation}__gt": 0}).order_by('ObservationDate')

        if covid_data.exists():
            covid_data = pd.DataFrame(
                covid_data.values('ObservationDate', observation))
            covid_data['Date'] = pd.to_datetime(covid_data['ObservationDate'])
            covid_data = covid_data.groupby('ObservationDate')[
                observation].sum().reset_index()
            covid_data['Country'] = selected_country

            all_data.append(covid_data)

    if all_data:
        combined_data = pd.concat(all_data)

        fig = px.line(combined_data, x='ObservationDate', y=observation,
                      color='Country',
                      title=f'{observation}', template='simple_white')
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        fig.update_layout(hovermode='x unified')
        fig.update_traces(
            hovertemplate='Date: %{x|%Y-%m-%d}<br>%{observation}: %{y}')
        fig.update_layout(title_x=0.5, xaxis_title="Date",
                          yaxis_title=f"{observation}")
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        config = {'displayModeBar': False}
        plot_div = plot(fig, config=config, output_type='div',
                        include_plotlyjs=False)

        return plot_div
    else:
        return None


if __name__ == '__main__':
    pass
