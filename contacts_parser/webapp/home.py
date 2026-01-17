import sys

import pandas as pd

import streamlit as st

from contacts_parser import conf
from contacts_parser.parsers import pandas_toolbox as pt

st.set_page_config(
    page_title="Statut des classes",
    page_icon="🏫",
    layout="wide",
    menu_items={
        'Get Help': "https://github.com/dad3zero/pyAPE/blob/master/README.md",
        'Report a bug': "https://github.com/dad3zero/pyAPE/issues",
        'About': "Application de gestion de contacts - Usage interne uniquement"
    }
)

# Arguments passed from CLI via sys.argv
file_path = sys.argv[1] if len(sys.argv) > 1 else None
separator = sys.argv[2] if len(sys.argv) > 2 else conf.CSV_SEPARATOR

# Load data from CLI argument or file uploader
if file_path:
    parents_data = pt.load_dataframe(file_path, sep=separator)
else:
    parents_file = st.file_uploader("Chemin vers le fichier des élèves")
    if parents_file:
        parents_data = pt.load_dataframe(parents_file, sep=separator)
    else:
        parents_data = None
        st.write("En attente du chargement de fichier.")

if parents_data is not None:
    parents_data = parents_data[parents_data['DIV.'].notnull()].sort_values(by=['DIV.', 'NOM'])
    st.session_state['parents_data'] = parents_data

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
