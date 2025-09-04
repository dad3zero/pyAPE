import streamlit as st

st.set_page_config(
    page_title="Détail des classes",
    page_icon="🏫",
    layout="wide",
)


if "parents_data" in st.session_state:
    grades = st.session_state['parents_data'].groupby('DIV.')

    st.title("Information classe")
    grade_selected = st.selectbox("Classe : ", grades)
    if grade_selected:
        current_class = grades.get_group(grade_selected)

        info1, info2 = st.columns(2)
        info1.metric(label="Élèves", value=len(current_class))
        info2.metric(label="Sans coordonnées", value=len(current_class[(current_class["NOM LEGAL"].isnull())
                                                                       & current_class[
                                                                           'NOM AUTRE LEGAL'].isnull()].sort_values(
            by=['NOM'])))

        st.dataframe(current_class[["NOM", "PRENOM"]].sort_values(by=['NOM']))
else:
    st.warning("Aucune donnée chargée. Retournez à la page d'accueil.")
