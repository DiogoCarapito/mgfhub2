import streamlit as st
from utils.etl import etl_xlsx
#from utils.graphs import graph_indicador


def main():
    """Main page content"""

    st.set_page_config(layout="wide")

    st.session_state["uploaded_file"] = None

    with st.sidebar:
        st.title("Upload")
        st.session_state["uploaded_file"] = st.file_uploader(
            "Upload de excel proveniente do MIMUF",
            type=["xlsx"],
            accept_multiple_files=False,
            help="Ajuda",
        )

        if st.session_state["uploaded_file"] is None:
            pass
            
        if st.session_state["uploaded_file"] is not None:
            main_df = etl_xlsx(st.session_state["uploaded_file"])
            list_med = ["Unidade"] + main_df["Medico Familia"].unique().tolist()[:-1] + ["Todos os Médicos"]
            #list_indicadores = ["Todos"] + main_df["Indicador"].unique().tolist()
            list_area_clinica = ["Todas"] + main_df["area_clinica"].unique().tolist()

            st.sidebar.title("Filtros")
            
            st.sidebar.subheader("Selecione o médico de família")
            med = st.sidebar.selectbox("Médico", list_med)
            
            st.sidebar.subheader("Selecione a área clínica")
            area_clinica = st.sidebar.selectbox("Área Clínica", list_area_clinica)


    st.title("mgfhub 2.0")

    if st.session_state["uploaded_file"] is None:
        st.warning("<== Por favor, faça o upload do ficheiro excel")
        
        with st.expander("Como estrair o fichero excel necessário?", expanded=False):
            st.write("1. Abrir o MIM@UF na sua Unidade de Saúde")
            st.write("2. Ir à pasta Indicadores")
            st.write("...")

        st.stop()

    if st.session_state["uploaded_file"] is not None:

        # Filter dataframe
        if med != "Todos os Médicos":
            main_df = main_df[main_df["Medico Familia"] == med]
        elif med == "Unidade":
            main_df.drop("Medico Familia", axis=1, inplace=True)
            
        if area_clinica != "Todas":
            main_df = main_df[main_df["area_clinica"] == area_clinica]

        #st.write(main_df.iloc[1].to_dict())

        vis = st.radio("Escolha o tipo de visualização", ["Tabela", "Dataframe"], horizontal=True)
   
        if vis == "Tabela":
            st.table(main_df)
        elif vis == "Dataframe":
            st.dataframe(main_df)

        

        # Graphs
        #graph_indicador(main_df.loc[0].to_dict())
        #graph_indicador(
            #{"id": 1, "nome_indicador": "teste", "min_aceitavel": 50, "min_esperado": 70, "max_esperado": 100, "max_aceitavel": 100, "Cumprimento": 60})

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
