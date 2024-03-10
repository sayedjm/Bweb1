import os

import django
import pandas as pd
import plotly.express as px
from plotly.offline import plot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from dashboard.models import CovidData


def get_county_heatmap(country, observation):
    df = pd.DataFrame(CovidData.objects.filter(Country=country).values())
    df['Date'] = pd.to_datetime(df['ObservationDate'])
    df_grouped = df.groupby("ObservationDate")[observation].sum().reset_index()
    df_grouped['Daily'] = df_grouped[observation].diff().fillna(
        df_grouped[observation])
    df_grouped['Daily'] = df_grouped['Daily'].clip(lower=0)
    df = pd.merge(df, df_grouped[['ObservationDate', 'Daily']],
                  on='ObservationDate', how='left')
    df['DayOfWeek'] = df['Date'].dt.strftime('%A')
    df['Week'] = df['Date'].dt.strftime('%U')
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Year'] = df['Date'].dt.strftime('%Y')
    df = df.groupby("ObservationDate").agg(
        {'DayOfWeek': 'first', 'Week': 'first', 'Month': 'first',
         'Year': 'first', 'Daily': 'max'}).reset_index()
    df = df.sort_values(by=['Year', 'Week'], ascending=[True, True])
    fig = px.density_heatmap(df,
                             x='Week',
                             y='DayOfWeek',
                             z='Daily',
                             facet_col='Year',
                             title=f"Corona heatmap {observation} cases ",
                             labels={
                                 'Daily': 'Number of Confirmed Cases'},
                             category_orders={
                                 'DayOfWeek': ['Monday', 'Tuesday',
                                               'Wednesday', 'Thursday',
                                               'Friday', 'Saturday', 'Sunday'],
                                 'Week': [str(week).zfill(2) for week in
                                          range(0, 53)]
                             },
                             color_continuous_scale="PuBu"

                             )
    fig.update_traces(hovertemplate='Confirmed: %{z}')

    fig.update_layout(title_x=0.5, coloraxis_colorbar_title_text='Count')
    config = {'displayModeBar': False}

    plot_div = plot(fig, config=config, output_type='div',
                    include_plotlyjs=False)
    return plot_div


if __name__ == '__main__':
    pass
