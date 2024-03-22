# Corona Dashboard - Django App Bweb1

## Introduction
This Django app serves as a Corona Dashboard, providing visualizations and information related to COVID-19 data.
It includes features like dynamic country-wise visualizations, worldwide statistics, and article scraping from PubMed.

## Setup Instructions

### Prerequisites
- Anaconda installed
- Python installed

### Installation Steps

1. Run the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to [http://localhost:8000/](http://localhost:8000/) to access the Corona Dashboard.

## Usage
- Upon accessing the dashboard, you can explore various features:
  - **Worldwide Statistics**: View global COVID-19 statistics and a worldwide map.
  - **Country-wise Plots**: Explore detailed visualizations for specific countries.
  - **Article Scraper**: Retrieve articles related to Sarscov2 from PubMed.
  - **Export Data**: Export data from the dashboard.

## Main Components
### `views.py`
- `home`: Renders the homepage and handles POST requests for navigation.
- `get_country_plots`: Generates visualizations for a randomly selected country.
- `get_plots`: Generates visualizations for a specified country.
- `get_data`: Handles data retrieval for multiple selected countries.
- `export_data`: Exports data from the dashboard.
- `pubmed_scraper_data`: Retrieves articles from PubMed.
- `info`: Renders the information page.

### Important Files
- `dashboard/models.py`: Defines the data models, including `CovidData`.
- `dashboard/python_script`: Contains scripts for data scraping, API calls, and plot generation.
- `dashboard/templates`: Holds HTML templates for rendering pages.


## Acknowledgments
- The dashboard uses Django for web development.
- Data visualizations are generated using Python scripts and the library Plotly.

---
