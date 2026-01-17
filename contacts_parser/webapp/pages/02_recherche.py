import streamlit as st

st.set_page_config(
    page_title="Recherche",
    page_icon="🔎",
    layout="wide",
)


if "parents_data" in st.session_state:
    parents_data = st.session_state['parents_data']

    st.title('Recherche parent par adresse mail')
    lookup_address = st.text_input('Recherche parent', max_chars=254)
    if lookup_address:
        info_from_address = parents_data.loc[(parents_data["COURRIEL LEGAL"] == lookup_address)
                                             | (parents_data["COURRIEL AUTRE LEGAL"] == lookup_address)]
        st.dataframe(info_from_address)
    else:
        st.write("Pas de sélection d'adresse de recherche")

    st.title('Recherche par nom')
    lookup_name = st.text_input('Recherche Nom', max_chars=100)
    if lookup_name:
        if len(lookup_name) < 2:
            st.warning("Veuillez entrer au moins 2 caractères")
        else:
            info_from_name = parents_data.loc[
                parents_data["NOM"].str.casefold().str.contains(
                    lookup_name.casefold(), regex=False, na=False
                )]
            st.dataframe(info_from_name)
    else:
        st.write("Pas de sélection nom de recherche")

else:
    st.warning("Aucune donnée chargée. Retournez à la page d'accueil.")
