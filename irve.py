import pandas as pd
import numpy as np
import sys
import pathlib
import plotly.express as px
import plotly.io as pio
from IPython.display import display, Markdown

pio.templates.default = "plotly_dark"

labels = {
    "nom_amenageur": "Nom amenageur"
    ,"nom_operateur": "Nom opérateur"
    ,"nom_enseigne": "Nom enseigne"
    ,"mis_en_service_cette_annee": "Mise en service en 2023"
    ,"date_mise_en_service": "Date de mise en service"
    ,"puissance_nominale_cat": "Puissance nominale"
    ,"prise_type_combo_ccs": "Possède une prise combo"
    ,"prise_type_2": "Possède une prise type 2"
}


df = pd.read_csv("data/consolidation-etalab-schema-irve-statique-v-2.2.0-20231130.csv" 
                ,low_memory=False
                ,parse_dates=["date_mise_en_service"]
                ,dtype={"consolidated_code_postal": str
                       })\
  .sort_values(['id_pdc_itinerance', 'last_modified'])\

df_filter = df["id_pdc_itinerance"]=="Non concerné"

df = pd.concat([
  df[~df_filter].drop_duplicates('id_pdc_itinerance', keep='last'),
  df[df_filter]
])

# Date de mise en service
df.loc[df["date_mise_en_service"]<pd.to_datetime("2010-01-01"),"date_mise_en_service"]=None
df["mis_en_service_cette_annee"] = np.where(df["date_mise_en_service"].dt.year==pd.to_datetime("now").year 
         , "Oui"
         , "Non")


# Département
df_dep = pd.read_csv("Data/departements-france.csv"
                     ,dtype={"code_departement": str})
df["code_departement"] = df["consolidated_code_postal"].str[:2]

df = pd.merge(df,df_dep, how='left', on='code_departement')

# Power
df["puissance_nominale_cat"] = pd.cut(\
  df["puissance_nominale"]\
  .apply(lambda x: x/1000 if x >1000 else x)\
,[0,1.8,3.5,7.5,26,52,151,500]
,labels=["1.7","3.4","7.5","22","50","150",">150"]
, include_lowest=False)

df["prise_type_combo_ccs"] = df["prise_type_combo_ccs"].str.lower().map({"0":"Non","false":"Non","1":"Oui","true":"Oui"})
df["prise_type_2"] = df["prise_type_2"].str.lower().map({"0":"Non","false":"Non","1":"Oui","true":"Oui"})
