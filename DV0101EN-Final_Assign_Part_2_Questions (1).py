#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Automobile Statistics Dashboard', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'left', 'color': '#000000', 'font-size': 20}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select Statistics',
            value='Yearly Statistics'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='1980',
            placeholder='Select Year'
        )
    ]),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

# Callback to update the year dropdown based on selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # Enable year dropdown for Yearly Statistics
    elif selected_statistics == 'Recession Period Statistics':
        return True  # Disable year dropdown for Recession Period Statistics
    else:
        return False  # Enable year dropdown by default

# Callback to update the output container based on selected year and statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using a line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Automobile sales fluctuate over Recession Period"
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a bar chart
        vehicle_data = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                vehicle_data,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average number of vehicles sold by vehicle type during Recession'
            )
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertising Expenditure Share by Vehicle Type during Recession'
            )
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2]),
            html.Div(className='chart-item', children=[R_chart3])
        ]
    elif selected_statistics == 'Yearly Statistics' and input_year:
        # Filter the data for the selected year
        yearly_data = data[data['Year'] == int(input_year)]

        # Plot 1: Yearly Automobile sales using a line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales using Line Chart"
            )
        )

        # Plot 2: Total Monthly Automobile sales using line chart
        # You should complete this part

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
            )
        )

        # Plot 4: Total Advertising Expenditure for each vehicle using a pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertising Expenditure by Vehicle Type in the year {}'.format(input_year)
            )
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1]),
            # Add code for Plot 2
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4])
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)