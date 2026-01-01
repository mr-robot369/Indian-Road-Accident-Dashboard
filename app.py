# !---- Importing necessary packages ----
import pandas as pd
import requests
from dash import Dash, dcc, html, Input, Output
from roadintel.charts import (
    create_monthly_trend_chart,
    create_state_bar_chart,
    create_severity_donut_chart,
    create_road_type_chart,
    create_vehicle_bar_chart,
    create_alcohol_pie_chart,
    create_weather_light_chart,
    create_india_map_chart,
    create_empty_map,
    calculating_insights,
    create_age_casualty_bar_chart
)

# !---- Loading the dataset ----
df = pd.read_csv('data/accident_preprocessed.csv')

# Create 'Accident Count' for aggregation
df['Accident Count'] = 1

# !---- Creating Lists for All Filters ----

# Location
all_states = sorted(df['State Name'].dropna().unique())
all_cities = sorted(df['City Name'].dropna().unique())

# Time
all_years = sorted(df['Year'].dropna().unique())
all_months = sorted(df['Month'].dropna().unique())
all_day_of_week = sorted(df['Day of Week'].dropna().unique())     
all_parts_of_day = sorted(df['Part of Day'].dropna().unique())

# Accident
all_accident_severity = sorted(df['Accident Severity'].dropna().unique())

# Road Condition
all_road_types = sorted(df['Road Type'].dropna().unique())

# Weather
all_weather_conditions = sorted(df['Weather Conditions'].dropna().unique())
all_lighting_conditions = sorted(df['Lighting Conditions'].dropna().unique())

# Driver
all_driver_age_categories = sorted(df['Driver Age Category'].dropna().unique())
all_alcohol_involvement = sorted(df['Alcohol Involvement'].dropna().unique())

# Vehicle
all_vehicle_types = sorted(df['Vehicle Type Involved'].dropna().unique())

# !---- Global Variables ----
# Set Global Plotly Template
template = 'plotly_dark'

# GeoJSON URL for the Geohacker India map
geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"

# --- Load GeoJSON directly once ---
geojson_data = requests.get(geojson_url).json()

# !---- Initialize the Dash App ----
app = Dash(__name__)
server = app.server

# !---- Dashboard layout ----
app.layout = html.Div(children=[
    
    # Section 1 : Title
    html.Section(className='header', children = [
        html.H1(
            'Indian Road Accident Dashboard',
            className='dashboard-title'
        ),
        html.P(
            'An interactive tool for analyzing accident patterns and high-risk conditions.',
            className='dashboard-subtitle'
        )
    ]),
    
    # Section 2 : sidebar + main content
    html.Div(className='content-container', children=[
    
        # Left Sidebar : filter
        html.Div(className='sidebar', children=[

            # -- Time filter --
            html.Div(className='filter-column-time', children=[
                html.H4('⏱️ TIME FILTERS', className='filter-heading-time'),

                html.Label('Select Year(s):', className='filter-label'),
                dcc.Dropdown(
                    id='year-filter',
                    options=[{'label': y, 'value': y} for y in all_years],
                    value=all_years,
                    multi=True,
                    className='filter-dropdown'
                ),

                html.Label('Select Month(s):', className='filter-label'),
                dcc.Dropdown(
                    id='month-filter',
                    options=[{'label': m, 'value': m} for m in all_months],
                    value=all_months,
                    multi=True,
                    className='filter-dropdown'
                ),

                html.Label('Select Day(s) of Week:', className='filter-label'),
                dcc.Dropdown(
                    id='dow-filter',
                    options=[{'label': d, 'value': d} for d in all_day_of_week],
                    value=all_day_of_week,
                    multi=True,
                    className='filter-dropdown'
                ),

                html.Label('Select Part of Day:', className='filter-label'),
                dcc.Dropdown(
                    id='part-of-day-filter',
                    options=[{'label': pod, 'value': pod} for pod in all_parts_of_day],
                    value=all_parts_of_day,
                    multi=True,
                    className='filter-dropdown'
                ),
            ]),

            # -- Location filter --
            html.Div(className='filter-column-location', children=[
                html.H4('📌 LOCATION FILTERS', className='filter-heading-location'),

                html.Label('Select State(s):', className='filter-label'),
                dcc.Dropdown(
                    id='state-filter',
                    options=[{'label': s, 'value': s} for s in all_states],
                    value=all_states,
                    multi=True,
                    className='filter-dropdown'
                ),

                html.Label('Select City:', className='filter-label'),
                # Dynamic options based on State
                dcc.Dropdown(
                    id='city-filter',
                    # options=[{'label': c, 'value': c} for c in all_cities],
                    value=[],   # Initially empty
                    multi=True,
                    className='filter-dropdown'
                ),
            ]),

            # -- Accident filters --
            html.Div(className='filter-column-accident', children=[
                html.H4('🚨 ACCIDENT FILTERS', className='filter-heading-accident'),

                html.Label('Accident Severity:', className='filter-label'),
                dcc.Dropdown(
                    id='severity-filter',
                    options=[{'label': sev, 'value': sev} for sev in all_accident_severity],
                    value=all_accident_severity,
                    multi=True,
                    className='filter-dropdown'
                ),

                html.Label('Road Type:', className='filter-label'),
                dcc.Dropdown(
                    id='road-type-filter',
                    options=[{'label': r, 'value': r} for r in all_road_types],
                    value=all_road_types,
                    multi=True,
                    className='filter-dropdown'
                )
            ]),
            
            # --- Weather filters ---
            html.Div(className='filter-column-climate', children=[
                html.H4('🌦️ CLIMATE FILTERS', className='filter-heading-climate'),

                html.Label('Weather Condition:', className='filter-label'),
                dcc.Dropdown(
                    id='weather-filter',
                    options=[{'label': w, 'value': w} for w in all_weather_conditions],
                    value=all_weather_conditions,
                    multi=True,
                    className='filter-dropdown'
                ),

                html.Label('Lighting Condition:', className='filter-label'),
                dcc.Dropdown(
                    id='lighting-filter',
                    options=[{'label': l, 'value': l} for l in all_lighting_conditions],
                    value=all_lighting_conditions,
                    multi=True,
                    className='filter-dropdown'
                ),
            ]),
            
            # --- Driver filters ---
            html.Div(className='filter-column-driver', children=[
                html.H4('👨‍✈️ DRIVER FILTERS', className='filter-heading-driver'),

                html.Label('Driver Age Category:', className='filter-label'),
                dcc.Dropdown(
                    id='driver-age-filter',
                    options=[{'label': a, 'value': a} for a in all_driver_age_categories],
                    value=all_driver_age_categories,
                    multi=True,
                    className='filter-dropdown'
                ),

                html.Label('Alcohol Involvement:', className='filter-label'),
                dcc.Dropdown(
                    id='alcohol-filter',
                    options=[{'label': alc, 'value': alc} for alc in all_alcohol_involvement],
                    value=all_alcohol_involvement,
                    multi=True,
                    className='filter-dropdown'
                ),
            ]),
            
            # --- Vehicle filters ---
            html.Div(className='filter-column-vehicle', children=[
                html.H4('🚗 VEHICLE FILTERS', className='filter-heading-vehicle'),

                html.Label('Vehicle Type:', className='filter-label'),
                dcc.Dropdown(
                    id='vehicle-type-filter',
                    options=[{'label': v, 'value': v} for v in all_vehicle_types],
                    value=all_vehicle_types,
                    multi=True,
                    className='filter-dropdown'
                ),
            ]),
        ]), # End of Sidebar
        
        # Right Side : KPIs & GRAPHS
        html.Div(className='main-content', children=[
            
            # Section 1 : KPIs
            html.Div(className='kpi-row', children=[
                html.Div(id='kpi-total-accidents', className='kpi-card'),
                html.Div(id='kpi-total-casualties', className='kpi-card'),
                html.Div(id='kpi-total-fatalities', className='kpi-card'),
                html.Div(id='kpi-fatality-rate', className='kpi-card'),
            ]),
            
            # Section 1 : Map (Row 1)
            html.Div(className='map-row', children=[
                # Use your new 'map-card' class for the child
                html.Div(className='map-card', children=[
                    dcc.Graph(id='india-map-chart', style={'height': '100%'})
                ])
            ]),
            
            # Section 2 : Charts (Row 2)
            html.Div(className='chart-row', children=[
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='accident-trend')
                ]),
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='states-accident')
                ])
            ]),

            # Section 3 : Charts (Row 3)
            html.Div(className='chart-row', children=[
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='accident-severity')
                ]),
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='road-severity')
                ])
            ]),
            
            # Section 4 : Charts (Row 4)
            html.Div(className='chart-row', children=[
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='accident-vehicle')
                ]),
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='alcohol-involvement')
                ])
            ]),

            # Section 5 : Charts (Row 5)
            html.Div(className='chart-row', children=[
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='weather_lightning')
                ]),
                html.Div(className='chart-card', children=[
                    dcc.Graph(id='driver_age_casualty')
                ])
            ]),

            # Section 6 : Insights
            html.Div(className='insight-row', children=[
                html.Div(className='insight-card', children=[
                    html.H3("Summary & Insights"),
                    html.Ul(children=[
                        html.Li(id='insight-1', children="Loading..."),
                        html.Li(id='insight-2', children="Loading..."),
                        html.Li(id='insight-3', children="Loading..."),
                        html.Li(id='insight-4', children="Loading...")
                    ]),
                    html.P(id='insight-conclusion', className='conclusion', children="Loading conclusion...")
                ])
            ])
            
        ]) # End of Main Content
        
    ]) # End of Content Container
]) # End of App

# ! ---- Callbacks ----
# ! 1. Cities Dropdown Callback
# Dynamic city selection based on selected states
# This only update the 'options' not 'value' as City Name column contain many NULL rows
@app.callback(
    Output('city-filter', 'options'),
    # Output('city-filter', 'value'),
    Input('state-filter', 'value'),
)
def set_city_options(selected_states):
    if not selected_states:
        # If no states are selected, return no options
        return []
    
    # Find all cities that are in the selected states
    cities_for_states = sorted(df[df['State Name'].isin(selected_states)]['City Name'].dropna().unique())
    
    # Return the new list of options
    new_options = [{'label': c, 'value': c} for c in cities_for_states]
    
    return new_options

# ! 2. KPI & Graphs Callback
@app.callback(
    [
        #! ------------------ KPI ------------------
        Output('kpi-total-accidents', 'children'),
        Output('kpi-total-casualties', 'children'),
        Output('kpi-total-fatalities', 'children'),
        Output('kpi-fatality-rate', 'children'),
        #! ------------------ Maps & Graphs ------------------
        Output('india-map-chart', 'figure'),
        Output('accident-trend', 'figure'),
        Output('states-accident', 'figure'),
        Output('accident-severity', 'figure'),
        Output('road-severity', 'figure'),
        Output('accident-vehicle', 'figure'),
        Output('alcohol-involvement', 'figure'),
        Output('weather_lightning', 'figure'),
        Output('driver_age_casualty','figure'),
        #! ------------------ Insights ------------------
        Output('insight-1', 'children'),
        Output('insight-2', 'children'),
        Output('insight-3', 'children'),
        Output('insight-4', 'children'),
        Output('insight-conclusion', 'children')
    ],
    [
        # Time Filters
        Input('year-filter', 'value'),
        Input('month-filter', 'value'),
        Input('dow-filter', 'value'),
        Input('part-of-day-filter', 'value'),
        # Location Filters
        Input('state-filter', 'value'),
        Input('city-filter', 'value'),
        # Accident Filters
        Input('severity-filter', 'value'),
        Input('road-type-filter', 'value'),
        # Climate Filters
        Input('weather-filter', 'value'),
        Input('lighting-filter', 'value'),
        # Driver Filters
        Input('driver-age-filter', 'value'),
        Input('alcohol-filter', 'value'),
        # Vehicle Filters
        Input('vehicle-type-filter', 'value')
    ]
)
def update_kpi(sel_years, sel_months, sel_week, sel_pod, sel_states, sel_cities, 
               sel_severity, sel_road_type, sel_weather, sel_lighting, 
               sel_driver_age, sel_alcohol, sel_vehicle_type):
    
    # 1) Selecting Dataframe
    dff = df[
        (df['Year'].isin(sel_years)) &
        (df['Month'].isin(sel_months)) &
        (df['Day of Week'].isin(sel_week)) &
        (df['Part of Day'].isin(sel_pod)) &
        (df['State Name'].isin(sel_states)) &
        (df['Accident Severity'].isin(sel_severity)) &
        (df['Road Type'].isin(sel_road_type)) &
        (df['Weather Conditions'].isin(sel_weather)) &
        (df['Lighting Conditions'].isin(sel_lighting)) &
        (df['Driver Age Category'].astype(str).isin(sel_driver_age)) &  # Converts category to string for matching
        (df['Alcohol Involvement'].isin(sel_alcohol)) &
        (df['Vehicle Type Involved'].isin(sel_vehicle_type))
    ].copy()

    if sel_cities:
        # for initial there is no city
        # if someone select any city mannually
        dff = dff[dff['City Name'].isin(sel_cities)]
        
    # 2) Handling Empty DataFrame
    if dff.empty:
        empty_kpi = [html.H3("-"), html.P("No Data")]

        # empty map
        empty_map = create_empty_map(dff, geojson_data, template)
        
        # return fig_empty
        empty_fig = {
            "layout": {
                "title": "No data for selected filters",
                "plot_bgcolor": "#222222",
                "paper_bgcolor": "#222222",
                "font_color": "#FFFFFF"
            }
        }
        return empty_kpi, empty_kpi, empty_kpi, empty_kpi, empty_map, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    # 3) Calculate KPIs
    total_accidents = len(dff)
    total_casualties = dff['Number of Casualties'].sum()
    total_fatalities = dff['Number of Fatalities'].sum()
    fatality_rate = (total_fatalities / total_casualties) * 100 if total_casualties > 0 else 0

     # 4) Formated KPIs
    kpi_acc = [html.H3(f"{total_accidents:,}", className='kpi-value-accent'), html.P("Total Accidents")]
    kpi_cas = [html.H3(f"{total_casualties:,}"), html.P("Total Casualties")]
    kpi_fat = [html.H3(f"{total_fatalities:,}"), html.P("Total Fatalities")]
    kpi_rate = [html.H3(f"{fatality_rate:.2f}%"), html.P("Fatality Rate")]

    # ----------------- Graph -----------------

    # --- 1. Indid's map ---
    fig_map = create_india_map_chart(dff, geojson_data, template)

    # --- 2. Monthly Accident Trend ---
    fig_monthly = create_monthly_trend_chart(dff, template)

    # --- 3. Top 10 States by Accident Count ---
    fig_state = create_state_bar_chart(dff, template)

    # --- 4. Accident Severity Distribution chart ---
    fig_severity = create_severity_donut_chart(dff, template)

    # --- 5. Accident Severity by Road Type ---
    fig_severity_road = create_road_type_chart(dff, template)

    # --- 6. Top 5 Vehicle Types Involved ---
    fig_vehicle = create_vehicle_bar_chart(dff, template)

    # --- 7. Alcohol Involvement ---
    fig_alcohol = create_alcohol_pie_chart(dff, template)

    # --- 8. Weather & Lightning Impact ---
    fig_weather = create_weather_light_chart(dff, template)

    # --- 9. Driver Age VS Casualty ---
    fig_age_casualty = create_age_casualty_bar_chart(dff, template)

    # ----------------- Insights -----------------
    insight_1, insight_2, insight_3, insight_4, conclusion = calculating_insights(dff)
    
    return (
        # ---- KPIs ----
        kpi_acc, kpi_cas, kpi_fat, kpi_rate, 
        # ---- Map & Graphs ----
        fig_map, fig_monthly, fig_state, fig_severity, fig_severity_road, fig_vehicle, fig_alcohol, fig_weather, fig_age_casualty,
        # ---- Insights ----
        insight_1, insight_2, insight_3, insight_4, conclusion
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7860,
        debug=False
    )