import pytest

import pandas as pd
import plotly.express as px

global_temperature = pd.read_csv('GlobalLandTemperatures/GlobalTemperatures.csv')
country_temperature = pd.read_csv('GlobalLandTemperatures/GlobalLandTemperaturesByCountry.csv')
country_name_iso = pd.read_csv('country_name_iso.csv')

@pytest.mark.parametrize('dataset, month',
                         [
                             (global_temperature,0),
                             (global_temperature,1),
                             (global_temperature,8),
                         ])
def plot_temperature_monthly(dataset,month=0):
    dataset['dt'] = pd.to_datetime(dataset['dt'])
    dataset['Year'] = dataset['dt'].dt.year
    dataset['Month'] = dataset['dt'].dt.month
    dataset = dataset[dataset['Year'] >= 1865]
    if month == 0:
        dataset_annual = dataset.groupby(['Year'],as_index=False).mean()
        fig = px.line(dataset_annual, x='Year', y='LandAverageTemperature',
                      title='1865 - 2015 Annual Land Average Temperature (Celsius)')
        fig.show()
    else:
        fig = px.line(dataset[dataset['Month']==month], x='dt', y='LandAverageTemperature',
                        title='1865 - 2015 Monthly Land Average Temperature (Celsius) in {}'.format(number_to_month(month)))
        fig.show()
    assert True


@pytest.mark.parametrize('dataset, year',
                         [
                             (country_temperature,1880),
                             (country_temperature,1950),
                             (country_temperature,2010),
                         ])
def geo_plot(dataset,year):
    dataset['dt'] = pd.to_datetime(dataset['dt'])
    dataset['Year'] = dataset['dt'].dt.year
    dataset['Month'] = dataset['dt'].dt.month
    dataset = dataset[dataset['Year'] >= 1865] #Only select 150 years from 1865 to 2015

    dataset_annual = dataset.groupby(['Country','Year'],as_index=False).mean()
    dataset_annual_iso = pd.merge(dataset_annual, country_name_iso, on='Country')

    fig = px.choropleth(dataset_annual_iso[dataset_annual_iso["Year"]==year],
                        locations="Iso_Alpha3",
                        color="AverageTemperature",
                        hover_name="Country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    assert True