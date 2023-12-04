import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash
import numpy as np
import sys
import pathlib
from datetime import datetime
import plotly.express as px
import plotly.io as pio
from IPython.display import display, Markdown

pio.templates.default = "plotly_dark"

df = pd.read_csv("data/consolidation-etalab-schema-irve-statique-v-2.2.0-20231130.csv" 
                ,low_memory=False
                ,parse_dates=["date_mise_en_service"])\
  .sort_values(['id_pdc_itinerance', 'last_modified'])\

df = pd.concat([
  df[df['id_pdc_itinerance']!="Non concerné"].drop_duplicates('id_pdc_itinerance', keep='last'),
  df[df['id_pdc_itinerance']=="Non concerné"]
])

df.loc[df["date_mise_en_service"]<pd.to_datetime("2010-01-01"),"date_mise_en_service"]=None

def Get_final_table():
    
    table_schema = pd.read_csv("Data/IRVE_itinerance_valide2023-05-24.csv").drop(columns=["Unnamed: 0","index"])
    table_schema.siren_amenageur = table_schema.siren_amenageur.astype(str)
    table_schema['code_departement'] = table_schema.consolidated_code_postal.apply(lambda x : str(x)[:2])
    
    
    table_depart = pd.read_csv("Data/departements-france.csv")


    res = pd.merge(table_schema,table_depart, how='inner', on='code_departement')
   
    return res 
    

def Show_repartition(table,group,by,first_elements):
    
    if not isinstance(table[group].tolist()[0],str):
        table[group] = table[group].astype(str)
    df = table.groupby(group)[by].count().reset_index(name="nombre total").sort_values(by="nombre total", ascending=False).head(first_elements)
    fig = px.bar(df, x=group, y="nombre total")
    return fig 


def Show_pdc_per_department(df):
    
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Visualisation des Points de Charge par Département en France"),

        # RadioButton pour choisir entre "aménageurs" et "enseigne"
        dcc.RadioItems(
            id='choice-radio',
            options=[
                {'label': 'Aménageurs', 'value': 'aménageurs'},
                {'label': 'Enseigne', 'value': 'enseigne'}
            ],
            value='aménageurs',
            labelStyle={'display': 'block'}
        ),

        # Dropdown qui change en fonction du choix du RadioButton
        dcc.Dropdown(id='dynamic-dropdown'),

        dcc.Graph(id='carte-pdc')
    ])

    @app.callback(
        Output('dynamic-dropdown', 'options'),
        Output('dynamic-dropdown', 'value'),
        Input('choice-radio', 'value')
    )
    def update_dropdown(choice):
        if choice == 'aménageurs':
            options = [{'label': amenageur, 'value': amenageur} for amenageur in df['nom_amenageur'].dropna().unique()]
            return options, options[0]['value']
        elif choice == 'enseigne':
            options = [{'label': enseigne, 'value': enseigne} for enseigne in df['nom_enseigne'].dropna().unique()]
            return options, options[0]['value']

    @app.callback(
        Output('carte-pdc', 'figure'),
        [Input('dynamic-dropdown', 'value'),
         Input('choice-radio', 'value'),
         Input('carte-pdc', 'relayoutData')]
    )
    def update_map(selected_value, choice, relayoutData):
        if choice == 'aménageurs':
            filtered_df = df[df['nom_amenageur'] == selected_value]
        elif choice == 'enseigne':
            filtered_df = df[df['nom_enseigne'] == selected_value]

        fig = px.choropleth_mapbox(filtered_df,
                                   geojson='https://france-geojson.gregoiredavid.fr/repo/departements.geojson',
                                   locations='code_departement',
                                   featureidkey="properties.code",
                                   color='nbre_pdc',
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",  
                                   zoom=5, center = {"lat": 46.603354, "lon": 1.888334},
                                   opacity=0.5,
                                   labels={'nbre_pdc':'Nombre de Points de Charge'})

        fig.update_layout(title=f'Points de Charge par Département pour {selected_value}',
                          margin={"r":0,"t":40,"l":0,"b":0},
                          mapbox=dict(bearing=0, pitch=0)
                         )
        return fig

    app.run_server(debug=True)


