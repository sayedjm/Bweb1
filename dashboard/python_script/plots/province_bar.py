
import os

import django
import pandas as pd
import plotly.express as px
from plotly.offline import plot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from dashboard.models import CovidData


def get_bar_province_state(country):
    covid_data = CovidData.objects.filter(Country=country)
    covid_data_df = pd.DataFrame(
        covid_data.values('Province_State', "Deaths", "Confirmed"))
    grouped_data = covid_data_df.groupby('Province_State')[
        ["Deaths", "Confirmed"]].max().reset_index()
    if grouped_data.empty:
        return None
    fig = px.bar(grouped_data, x='Province_State', y=["Deaths", "Confirmed"],
                 title=f'Cases by region', barmode='group', text_auto='.2s')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside",
                      cliponaxis=False)
    fig.update_layout(title_x=0.5, xaxis_title="Region", yaxis_title="Count",
                      legend_title_text='')
    config = {'displayModeBar': False}
    plot_div = plot(fig, config=config, output_type='div',
                    include_plotlyjs=False)

    return plot_div


if __name__ == '__main__':
    pass
