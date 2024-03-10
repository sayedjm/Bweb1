import os
from datetime import date

import pandas as pd
from dashboard.models import CovidData


def export(request):
    data_type = request.POST.get('file_export_type')
    count_country = request.POST.get('count_country')

    if count_country == '1':
        selected_country = "".join(request.POST.getlist('export_country'))
        covid_data_objects = CovidData.objects.filter(Country=selected_country)
        export_name = selected_country
    else:
        selected_country = request.POST.getlist('export_country')
        covid_data_objects = CovidData.objects.filter(Country__in=selected_country)
        export_name = "_".join(selected_country)

    covid_data_df = pd.DataFrame.from_records(covid_data_objects.values())

    if data_type == 'json':
        exported_data = covid_data_df.to_json(orient='records', indent=4)
        file_extension = 'json'
    elif data_type == 'tab':
        exported_data = covid_data_df.to_csv(sep='\t', index=False)
        file_extension = 'tsv'
    elif data_type == 'csv':
        exported_data = covid_data_df.to_csv(index=False)
        file_extension = 'csv'

    export_directory = 'dashboard/export/'
    today = date.today()

    file_name = f"{today}_{export_name}_covid_data.{file_extension}"
    file_path = os.path.join(export_directory, file_name)

    with open(file_path, 'w') as file:
        file.write(exported_data)
    return file_path


if __name__ == '__main__':
    pass
