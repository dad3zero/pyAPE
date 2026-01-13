import pandas as pd

import streamlit as st

from contacts_parser import conf
from contacts_parser.parsers import pandas_toolbox as pt

st.set_page_config(
    page_title="Statut des classes",
    page_icon="🏫",
    layout="wide",
)

parents_file = st.file_uploader("Chemin vers le fichier des élèves")

if parents_file:
    parents_data = pt.load_dataframe(parents_file, sep=conf.CSV_SEPARATOR)

    parents_data = parents_data[parents_data['DIV.'].notnull()].sort_values(by=['DIV.', 'NOM'])
    st.session_state['parents_data'] = parents_data

    # parents_data.info()

    per_class = parents_data['DIV.'].value_counts().sort_index()

    st.dataframe(per_class)

    no_parent1 = len(parents_data.loc[(parents_data["ADRESSE LEGAL"] == "Le responsable n'a pas souhaité communiquer ses coordonnées.")])

    no_parent2 = len(parents_data.loc[(parents_data["ADRESSE AUTRE LEGAL"] == "Le responsable n'a pas souhaité communiquer ses coordonnées.")])

    no_strict_parent2 = len(parents_data.loc[(parents_data["ADRESSE AUTRE LEGAL"].isnull())])

    no_value = len(parents_data[(parents_data["NOM LEGAL"].isnull())
                     & parents_data['NOM AUTRE LEGAL'].isnull()].sort_values(by=['NOM']))

    st.title("Enfants sans informations")
    total_kids, parent_info_1, parent_info_2, parent_info_3, no_parent_2 = st.columns(5)
    total_kids.metric(label="Total", value=len(parents_data))
    parent_info_1.metric(label="Absent Premier parent", value=no_parent1)
    parent_info_2.metric(label="Absent Second parent", value=no_parent2)
    parent_info_3.metric(label="Sans information", value=no_value)
    no_parent_2.metric(label="Pas Parent 2", value=no_strict_parent2)

else:
    st.write("En attente du chargement de fichier.")