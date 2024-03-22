import requests


def get_rest_county_data(g_selected_country):
    try:
        url = f'https://restcountries.com/v3.1/name/{g_selected_country}'
        response = requests.get(url)
        response.raise_for_status()

        if response.json():
            data = response.json()[0]
            return {
                "name": data.get("name", {}).get("common", None),
                "ISO3166": data.get("cca3", None),
                "region": data.get("region", None),
                "maps": data.get("maps", {}).get("googleMaps", None),
                "population": data.get("population", None),
                "flag": data.get("flag", None),
            }
        else:
            return {}
    except requests.exceptions.RequestException:
        return {}


if __name__ == '__main__':
    print(get_rest_county_data('China'))
