import pycountry


def convert_to_iso_alpha(iso3166_code):
    try:
        return pycountry.countries.get(alpha_2=iso3166_code).alpha_3
    except LookupError:
        return "No data available"
