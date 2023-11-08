import streamlit as st
from utils.etl import etl_bicsp, etl_mimuf_p02_01_R03
from utils.calc import calcular_idg, calcular_idg_maximo


def filter_df(df, filtro_area, filtro_sub_area):
    df = df[df["Área"].isin(filtro_area)]
    df = df[df["Sub-Área"].isin(filtro_sub_area)]
    return df


def main():
    # Configurations

    st.set_page_config(layout="wide")

    # create session state variables
    if "uploaded_file_bicsp" not in st.session_state:
        st.session_state["uploaded_file_bicsp"] = None
    if "uploaded_file_mimuf" not in st.session_state:
        st.session_state["uploaded_file_mimuf"] = None
    if "filtro_area" not in st.session_state:
        st.session_state["filtro_area"] = []

    # if "bicsp_table" not in st.session_state:
    #    st.session_state["bicsp_table"] = None

    # Sidebar

    with st.sidebar:
        st.title("Upload documentos")

        # upload de xlsx de mimuf

        # st.session_state["uploaded_file_mimuf"] = st.file_uploader(
        #    "Upload de excel proveniente do MIMUF",
        #    type=["xlsx"],
        #    accept_multiple_files=False,
        #    help="Ajuda MIMUF",
        # )

        # upload de xlsx de bicsp
        st.session_state["uploaded_file_bicsp"] = st.file_uploader(
            "Upload excel proveniente do BI-CSP",
            type=["xlsx"],
            accept_multiple_files=False,
            help="Ajuda BI-CSP",
        )

        # if st.session_state["uploaded_file_bicsp"] is not None:
        #    st.title("Filtros")

        #    df_bicsp = etl_bicsp(st.session_state["uploaded_file_bicsp"])

        #    lista_area = df_bicsp["Área"].unique().tolist()

        #    filtro_area = st.multiselect("Filtro por área", lista_area, default=lista_area)

        #    lista_sub_area = df_bicsp["Sub-Área"].unique().tolist()

        #    filtro_sub_area = st.multiselect("Filtro por sub área", lista_sub_area, default=lista_sub_area)

        # se existir um ficheiro excel do mimuf
        if st.session_state["uploaded_file_mimuf"] is not None:
            # executar etl do mimuf
            main_df = etl_mimuf_p02_01_R03(st.session_state["uploaded_file_mimuf"])

            # criar lista de médicos
            list_med = ["Unidade", "TODOS os Médicos"] + main_df[
                "Medico Familia"
            ].unique().tolist()

            # criar lista de áreas clínicas
            list_area_clinica = ["Todas"] + main_df["area_clinica"].unique().tolist()

            # filtros
            st.sidebar.title("Filtros")

            # filtros de médicos
            st.sidebar.subheader("Selecione o médico de família")
            med = st.sidebar.selectbox("Médico", list_med)

            # filtos de áreas clínicas
            st.sidebar.subheader("Selecione a área clínica")
            area_clinica = st.sidebar.selectbox("Área Clínica", list_area_clinica)

    # Main page content

    st.title("mgfhub 2.0")

    # texto para ajudar upload de excel se ainda não tiver sido feito
    if st.session_state["uploaded_file_bicsp"] is None:
        st.warning("<== Por favor, faça o upload do ficheiro excel")

        with st.expander(
            "Como estrair o fichero excel necessário do BI-CSP?", expanded=False
        ):
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                pass
            with col2:
                st.write(
                    "#### 1. Abrir o o [BI CSP](https://bicsp.min-saude.pt/pt/biselfservice/Paginas/home.aspx) e fazer login com as credenciais da ARS"
                )
                st.divider()

                st.write(
                    "#### 2. Ir ao separador dos **Indicadores | IDG** e selecionar o **IDG das Unidades Funcioinais**"
                )
                st.image("tutorial/tutorial_bicsp_1.png", use_column_width=True)
                st.divider()

                st.write("#### 3. Selecionar o separador **UF - IDG - Indicadores**")
                st.image("tutorial/tutorial_bicsp_2.png", use_column_width=True)
                st.divider()

                st.write("#### 4. Selecionar o **Mês** e a **Nome Unidade**")
                st.image("tutorial/tutorial_bicsp_3.png", use_column_width=True)
                st.divider()

                st.write(
                    "#### 5. Selecionar o botão **More Options** no canto superior direito da tabela pirncipal"
                )
                st.image("tutorial/tutorial_bicsp_4.png", use_column_width=True)
                st.divider()

                st.write("#### 6. Selecionar primeira opção **Export data**")
                st.image("tutorial/tutorial_bicsp_5.png", use_column_width=True)
                st.divider()

                st.write(
                    "#### 7. Selecionar a 3ª opção **Underlying data** e selecionar o botão **Export**"
                )
                st.image("tutorial/tutorial_bicsp_6.png", use_column_width=True)
                st.divider()

                st.write(
                    "#### 8. Fazert o uload do ficheiro excel gerado (pasta de transferencias) neste site no local destinado a upload"
                )
                st.image("tutorial/tutorial_bicsp_7.png", use_column_width=True)
            with col3:
                pass

    if st.session_state["uploaded_file_mimuf"] is not None:
        # execução de Filtros por médico e área clínica
        if med != "TODOS os Médicos":
            main_df = main_df[main_df["Medico Familia"] == med]
        elif med == "Unidade":
            main_df.drop("Medico Familia", axis=1, inplace=True)

        if area_clinica != "Todas":
            main_df = main_df[main_df["area_clinica"] == area_clinica]

        # número de indicadores
        st.write(f"Nº de indicadores: {main_df['id'].nunique()}")

        st.dataframe(main_df)

        st.metric("IDG", round(main_df["percentagem_final"].sum(), 2))

        main_df.to_csv("main_df.csv", index=False)

    # se excel bi_csp for carregado
    if st.session_state["uploaded_file_bicsp"] is not None:
        # etl do bi_csp
        bicsp_table = etl_bicsp(st.session_state["uploaded_file_bicsp"])

        # Filtros
        st.subheader("Filtros")

        with st.expander(
            "Filtros Área, Sub-Área, Dimensão e Indicador", expanded=False
        ):
            # Areas
            lista_areas = bicsp_table["Área"].unique().tolist()
            filtro_areas = st.multiselect(
                "Filtro por área",
                lista_areas,
                default=lista_areas,
            )
            bicsp_table = bicsp_table[bicsp_table["Área"].isin(filtro_areas)]

            # Sub-areas
            lista_sub_areas = bicsp_table["Sub-Área"].unique().tolist()
            filtro_sub_areas = st.multiselect(
                "Filtro por sub-área",
                lista_sub_areas,
                default=lista_sub_areas,
            )
            bicsp_table = bicsp_table[bicsp_table["Sub-Área"].isin(filtro_sub_areas)]

            # dimensões
            lista_dimensoes = bicsp_table["Dimensão"].unique().tolist()
            filtro_dimensoes = st.multiselect(
                "Filtro por dimensão",
                lista_dimensoes,
                default=lista_dimensoes,
            )
            bicsp_table = bicsp_table[bicsp_table["Dimensão"].isin(filtro_dimensoes)]

            # indicadores
            lista_indicadores = bicsp_table["id"].unique().tolist()
            filtro_indicadores = st.multiselect(
                "Filtro por indicador",
                lista_indicadores,
                default=lista_indicadores,
            )
            bicsp_table = bicsp_table[bicsp_table["id"].isin(filtro_indicadores)]

        col_slide_1, col_slide_2, col_slide_3 = st.columns(3)
        with col_slide_1:
            # slider com filtro do score
            filtro_score = st.slider(
                "Filtro de score",
                min_value=0.0,
                max_value=2.0,
                value=(0.0, 2.0),
                step=0.1,
                help="filtrar por score para excluir indicadores fora do intervalo selecionado",
            )

        with col_slide_2:
            # slider com filtro da percentangem_do_idg
            max_percent_idg = float(bicsp_table["percentagem_do_idg"].max())

            filtro_percentagem = st.slider(
                "Filtro de percentagem do IDG",
                min_value=0.0,
                max_value=max_percent_idg,
                value=(0.0, max_percent_idg),
                step=0.1,
                help="filtrar por impacto no IDG em percentagem para excluir indicadores fora do intervalo selecionado",
            )

        bicsp_table = bicsp_table[bicsp_table["Score"] >= filtro_score[0]]
        bicsp_table = bicsp_table[bicsp_table["Score"] <= filtro_score[1]]
        bicsp_table = bicsp_table[
            bicsp_table["percentagem_do_idg"] >= filtro_percentagem[0]
        ]
        bicsp_table = bicsp_table[
            bicsp_table["percentagem_do_idg"] <= filtro_percentagem[1]
        ]

        with col_slide_3:
            if st.checkbox("Incluir colunas: Área, Sub-Área e Diemnsão", value=False):
                pass
            else:
                bicsp_table = bicsp_table.drop(["Área", "Sub-Área", "Dimensão"], axis=1)
            if st.checkbox(
                "Incluir colunas de Intervalos Aceitáveis e Esperados", value=False
            ):
                pass
            else:
                bicsp_table = bicsp_table.drop(
                    ["Min. Aceit", " Min. Esper", "Máx. Esper", "Máx. Aceit"], axis=1
                )

        # Cálculos
        # numero de inidcadores
        numero_de_indicadores = bicsp_table["id"].nunique()

        # IDG actial
        idg_actual = calcular_idg(bicsp_table)

        # IDG máximo
        idg_maximo = calcular_idg_maximo(bicsp_table)

        # diferença entre idg maximo e idg actual
        diferenca_idg = round(idg_maximo - idg_actual, 2)

        # colunas visuais
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            st.metric(
                "Número indicadores",
                numero_de_indicadores,
                help="Número de indicadores selecionados",
            )

        with col_2:
            # calculo do IDG maximo
            st.metric(
                "IDG maximo possível",
                idg_maximo,
                help="IDG máximo possível dos indicadores selecionados",
            )

        with col_3:
            # calculo idg
            st.metric(
                "IDG calculado",
                idg_actual,
                help="IDG real calculado com base nos scores após aplicar os filtros selecionados",
            )

        with col_4:
            # percentamgem do idg maximo
            st.metric(
                "Diferença entre máximo e calculado",
                diferenca_idg,
                help="Diferença entre o IDG máximo e o IDG calculado dos indicadores selecionados. Corresponde ao potencial de ganho no IDG se os indicadores selecionados passarem a serem completamente cumpridos",
            )

        # remove columns

        st.dataframe(bicsp_table, use_container_width=True, hide_index=True)

        # button to download in csv
        st.download_button(
            label="Download tabela",
            data=bicsp_table.to_csv(index=False),
            file_name="bicsp_table.csv",
            mime="text/csv",
        )

        # save dataframe to csv
        # bicsp_table.to_csv("bicsp_table.csv", index=False)
        # save dataframe to csv


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
