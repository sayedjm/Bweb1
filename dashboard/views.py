from random import randint

from django.contrib import messages
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from dashboard.models import CovidData
from dashboard.python_script.data.pubmed_scraper import get_articles
from dashboard.python_script.data.rest_api import get_rest_county_data
from dashboard.python_script.data.export import export

from dashboard.python_script.plots.county_heatmap import get_county_heatmap
from dashboard.python_script.plots.line_plots import get_line_plot
from dashboard.python_script.plots.county_geo import get_county_geo_plot
from dashboard.python_script.plots.all_geo import get_all_geo_plot
from dashboard.python_script.plots.province_bar import get_bar_province_state
from dashboard.python_script.plots.pie_population import get_pie_population_plot
from dashboard.python_script.plots.pie_plot import get_pie_plot


def home(request):
    if request.method == 'POST':
        if request.POST.get("world-map"):
            return HttpResponseRedirect('table/')
        elif request.POST.get("random_country"):
            return HttpResponseRedirect('plot/')
        elif request.POST.get("articles"):
            return HttpResponseRedirect('articles/')
        elif request.POST.get('country'):
            selected_country = request.POST.get('country')
            context = get_plots(selected_country)
            return render(request, "country_plots.html", context)
        elif request.POST.get("file_export"):
            export_data(request)
            return HttpResponseRedirect('/')

    countries = sorted(list(CovidData.objects.values_list('Country', flat=True).distinct()))
    return render(request, "home.html", context={'countries': countries})


def get_country_plots(request):
    countries = sorted(list(CovidData.objects.values_list('Country', flat=True).distinct()))
    if request.method == 'POST':
        if request.POST.get("file_export"):
            export_data(request)
            return HttpResponseRedirect('/')
    else:
        selected_country = countries[randint(0, len(countries))]
        context = get_plots(selected_country)
        return render(request, "country_plots.html", context)

    return render(request, "country_plots.html")


def get_plots(selected_country):
    data_county = get_county_data(selected_country)
    population = data_county.get('population', None)

    if population:
        plot_one = get_pie_population_plot(selected_country, population)
    else:
        plot_one = get_pie_plot(selected_country)

    plot_confirmed = get_line_plot(selected_country, 'Confirmed')
    plot_deaths = get_line_plot(selected_country, 'Deaths')
    plot_recovered = get_line_plot(selected_country, 'Recovered')
    plot_geo = get_county_geo_plot(selected_country)
    plot_province_state = get_bar_province_state(selected_country)
    heatmap_confirmed = get_county_heatmap(selected_country, 'Confirmed')
    heatmap_deaths = get_county_heatmap(selected_country, 'Deaths')

    assert isinstance(plot_one, object)
    context = {'plot_bar': plot_one,
               'plot_confirmed': plot_confirmed,
               'plot_deaths': plot_deaths,
               'plot_recovered': plot_recovered,
               'plot_geo': plot_geo,
               'plot_province_state': plot_province_state,
               'data_county': data_county,
               'selected_country': selected_country,
               'count_country': 1,
               'heatmap_confirmed': heatmap_confirmed,
               'heatmap_deaths': heatmap_deaths,
               }

    return context


def get_data(request):
    if request.method == 'POST':
        if request.POST.get('selected_countries'):
            selected_countrys = request.POST.getlist('selected_countries')
            if len(selected_countrys) == 1:
                context = get_plots(selected_countrys[0])
                return render(request, "country_plots.html", context)
            else:
                plot_one = get_pie_plot(selected_countrys)
                plot_confirmed = get_line_plot(selected_countrys, 'Confirmed')
                plot_deaths = get_line_plot(selected_countrys, 'Deaths')
                plot_recovered = get_line_plot(selected_countrys, 'Recovered')
                plot_geo = get_county_geo_plot(selected_countrys)
                context = {'plot_bar': plot_one,
                           'plot_confirmed': plot_confirmed,
                           'plot_deaths': plot_deaths,
                           'plot_recovered': plot_recovered,
                           'plot_geo': plot_geo,
                           'data_county': {'name': 'Selected countrys'},
                           'selected_country': selected_countrys,
                           'count_country': len(selected_countrys)
                           }
                return render(request, "country_plots.html", context=context)
        elif request.POST.get("file_export"):
            export_data(request)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

    covid_data = CovidData.objects.values('Country', 'ISO3166_CountryCode').annotate(
        max_confirmed=Cast(Max('Confirmed'), IntegerField()),
        max_deaths=Cast(Max('Deaths'), IntegerField())
    ).order_by('-max_confirmed').values(
        'Country', 'ISO3166_CountryCode', 'max_confirmed', 'max_deaths'
    )
    plot_geo = get_all_geo_plot()
    context = {"covid_data": covid_data, 'plot_geo': plot_geo}
    return render(request, "worldwide_selection.html", context)


def get_county_data(g_selected_country):
    country_data = get_rest_county_data(g_selected_country)
    return country_data


def export_data(request):
    file_path = export(request)
    if file_path:
        messages.success(request, f"File exported successfully: {file_path}")
    return HttpResponseRedirect('/')


def pubmed_scraper_data(request):
    if request.GET:
        offset = int(request.GET.get('offset', 0))
        max_results = int(request.GET.get('max_results', 5))
        query = request.GET.get('query', 'Sarscov2')
        articles = get_articles(query=query, max_results=max_results, offset=offset)
        return JsonResponse(articles)
    return render(request, "articles.html")
