import streamlit as st
from utils.etl import etl_xlsx


def main():
    """Main page content"""

    st.set_page_config(layout="wide")

    st.title("mgfhub 2.0")

    # File uploader
    file_xlsx = st.file_uploader(
        "Upload de excel proveniente do MIMUF",
        type=["xlsx"],
        accept_multiple_files=False,
        help="Ajuda",
    )

    # Transform file into dataframe
    main_df = etl_xlsx(file_xlsx)

    list_med = ["Unidade"] + main_df["Medico Familia"].unique().tolist()
    

    list_indicadores = ["Todos"] + main_df["Indicador"].unique().tolist()

    # Sidebar
    st.sidebar.title("Menu")
    st.sidebar.subheader("Selecione o médico de família")
    med = st.sidebar.selectbox("Médico", list_med)
    

    indicadores = st.sidebar.multiselect("indicador", options=list_indicadores, default=list_indicadores[0])

    # Filter dataframe
    if med == "Unidade":
        main_df = main_df
    else:
        main_df = main_df[main_df["Medico Familia"] == med]
    
    if indicadores == "Todos":
        main_df = main_df
    else:
        main_df = main_df[main_df["Indicador"].isin(indicadores)]

    #medico selecionado
    st.write(med)
    #indicadores selecionados
    st.write(indicadores)

    st.table(main_df)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
