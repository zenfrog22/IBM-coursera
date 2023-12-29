# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                    options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',
                                    placeholder="Select a launch site here",
                                    searchable=True                               
                                )),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload]
                                )),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df
        names_label = 'Launch Site'
        values_label = 'class'
        title_label = 'Total Success Launches by Site'
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class',as_index=False).count()
        data['class'] = data['class'].apply(lambda x : 'Success' if x == 1 else 'Failure')
        names_label = 'class'
        values_label = 'Unnamed: 0'
        title_label = 'Total Success Launches for Site ' + entered_site

    fig = px.pie(data, values=values_label, 
        names=names_label, 
        title=title_label)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_success_payload_chart(entered_site, payload_range):
    filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] <= payload_range[1]) & (spacex_df['Payload Mass (kg)'] >= payload_range[0])]
    if entered_site == 'ALL':
        data = filtered_data
        title_label = 'Correlation between Payload and Success for All Sites'
    else:
        data = filtered_data[filtered_data['Launch Site'] == entered_site];
        title_label = 'Correlation between Payload and Success for Site ' + entered_site

    x_label = 'Payload Mass (kg)'
    y_label = 'class'
    color_label = 'Booster Version Category'

    return px.scatter(data, x=x_label, y=y_label, color=color_label, title=title_label)

# Run the app
if __name__ == '__main__':
    app.run_server()
