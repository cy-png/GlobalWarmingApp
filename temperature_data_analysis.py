import pandas as pd
import plotly.express as px


global_temperature = pd.read_csv('GlobalLandTemperatures/GlobalTemperatures.csv')
country_temperature = pd.read_csv('GlobalLandTemperatures/GlobalLandTemperaturesByCountry.csv')
country_name_iso = pd.read_csv('country_name_iso.csv')


# Transfer number to month for title in plot
def number_to_month(num):
    if num == 1:
        return "Jan"
    elif num == 2:
        return 'Feb'
    elif num == 3:
        return 'Mar'
    elif num == 4:
        return 'Apr'
    elif num == 5:
        return 'May'
    elif num == 6:
        return 'Jun'
    elif num == 7:
        return 'Jul'
    elif num == 8:
        return 'Aug'
    elif num == 9:
        return 'Sep'
    elif num == 10:
        return 'Oct'
    elif num == 11:
        return 'Nov'
    elif num == 12:
        return 'Dec'


# Line plot of global average temperature
# When month equals to 0, it means annual average temperature
def plot_temperature_monthly(dataset, month=0):
    dataset['dt'] = pd.to_datetime(dataset['dt'])
    dataset['Year'] = dataset['dt'].dt.year
    dataset['Month'] = dataset['dt'].dt.month
    dataset = dataset[dataset['Year'] >= 1865] #Only select 150 years from 1865 to 2015
    if month == 0:
        dataset_annual = dataset.groupby(['Year'],as_index=False).mean()
        fig = px.line(dataset_annual, x='Year', y='LandAverageTemperature',
                      title='1865 - 2015 Annual Land Average Temperature (Celsius)')
        fig.update_xaxes(title='Year')
    else:
        fig = px.line(dataset[dataset['Month']==month], x='dt', y='LandAverageTemperature',
                        title='1865 - 2015 Monthly Land Average Temperature (Celsius) in {}'.format(number_to_month(month)))
        fig.update_xaxes(title='Year ({} of every year)'.format(number_to_month(month)))
    return fig


# Geo Plot of Temperature by year
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
                        color_continuous_scale=px.colors.sequential.RdBu[::-1],
                        range_color=[-15,31])
    return fig
