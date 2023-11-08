"""
ETL pipeline for data processing
"""

import pandas as pd
from utils.indicador import id_indicador
from utils.calc import cumprimento_unidade, calc_score
from utils.utils import normalizacao_medico_familia, transform_to_float


def extrair_indicadores(df, nome_coluna):
    """
    Extrai os indicadores de um dataframe, dado o nome da coluna
    cria uma nova coluna com o id do indicador
    """
    df[nome_coluna] = df[nome_coluna].str.split(".").str[1]

    return df


def etl_mimuf_p02_01_R03(file):
    # open xlsx file
    df = pd.read_excel(file)

    # remove the 2 initial columns
    df = df.iloc[:, 2:]

    # remove the 3rd and 4th column
    df = df.drop(df.columns[[2, 3]], axis=1)

    # give a name to the 1st and 2nd columns
    df = df.rename(columns={df.columns[0]: "id_indicador", df.columns[1]: "indicador"})

    # processar id indicadores
    df = extrair_indicadores(df, "id_indicador")

    # remove indicador and ID id_Indicador
    df = df.drop(["indicador"], axis=1)

    # create a multiindex dataframe from the info in the header, 1st and 2nd row of df
    df.columns = pd.MultiIndex.from_tuples(zip(df.columns, df.iloc[0], df.iloc[1]))

    # remove the 1st and 2nd row
    df = df.iloc[2:]
    # reset index
    df = df.reset_index(drop=True)

    # df.set_index(df.columns(0), inplace=True)
    # remove the 1st header
    df.columns = df.columns.droplevel(0)

    df_stack = df.stack()

    df_index = df[df.columns[0]]

    # create a new column named indicador in df_stack, where its string comes from the correponding value that corresponds the index of df_index and df_stack
    df_stack["indicador"] = df_index[df_stack.index.get_level_values(0)].values

    df_stack.reset_index(inplace=True)

    # rename columns
    df_stack = df_stack.rename(columns={"level_1": "Medico Familia"})

    df_stack = normalizacao_medico_familia(df_stack)

    # convert indicador into int
    df_stack["id"] = df_stack["indicador"].astype(int)

    df_final = df_stack[
        [
            "id",
            "Medico Familia",
            "Den.",
            "Num.",
            "Valor",
        ]
    ]

    df_final = df_final.rename(
        columns={"Den.": "Total Utentes", "Num.": "Utentes Cumpridores"}
    )

    # Total Utentes and Utentes Cumpridores switch , to . and . to , and then to be int
    df_final = transform_to_float(
        df_final, ["Total Utentes", "Utentes Cumpridores", "Valor"]
    )

    df_final.sort_values(by=["id"], inplace=True)

    intervalos = pd.read_csv("data/indicadores_post_processed.csv")

    df_com_intervalos = pd.merge(df_final, intervalos, how="left", on="id")

    df_com_intervalos.dropna(inplace=True)

    df_com_intervalos = cumprimento_unidade(df_com_intervalos)

    df_com_intervalos = df_com_intervalos[
        [
            "id",
            "nome_abreviado",
            "area_clinica",
            "Medico Familia",
            "Total Utentes",
            "Utentes Cumpridores",
            "Valor",
            "min_aceitavel",
            "min_esperado",
            "max_esperado",
            "max_aceitavel",
        ]
    ]

    # sort dataframe by id in ascending order
    df_com_intervalos.sort_values(by=["id"], inplace=True)

    # remove rows that dont belong to a list of indicadores
    impacto_idg = pd.read_csv("data/usf_ucsp_indicadores_2022_comimpactoIDG.csv")
    impacto_idg = impacto_idg["id"].unique().tolist()
    df_com_intervalos = df_com_intervalos[df_com_intervalos["id"].isin(impacto_idg)]

    df_com_intervalos = calc_score(df_com_intervalos)

    # import a csv with the scores arlready calculated
    df_score = pd.read_csv("data/df_sunburst_pre_graph.csv")
    df_score = df_score[["id_indicador", "value"]]

    # rename id_indicador to id
    df_score = df_score.rename(columns={"id_indicador": "id", "value": "percentagem"})

    # merge the 2 dataframes so that df gets a new column where the ID is the same
    df_com_intervalos = pd.merge(df_com_intervalos, df_score, how="left", on="id")

    df_com_intervalos["percentagem_final"] = (
        df_com_intervalos["percentagem"] * df_com_intervalos["score"] / 2
    )

    return df_com_intervalos


def preprocess(df):
    # remove the 2 initial columns
    df = df.iloc[:, 2:]

    # remove the 3rd and 4th column
    df = df.drop(df.columns[[2, 3]], axis=1)

    # give a name to the 1st and 2nd columns
    df = df.rename(columns={df.columns[0]: "id_Indicador", df.columns[1]: "Indicador"})

    # merge the 2 columns
    df["Indicador"] = df["id_Indicador"].astype(str) + " - " + df["Indicador"]

    # remove indicador and ID id_Indicador
    df = df.drop(["id_Indicador"], axis=1)

    # create a multiindex dataframe from the info in the header, 1st and 2nd row of df
    df.columns = pd.MultiIndex.from_tuples(zip(df.columns, df.iloc[0], df.iloc[1]))

    # remove the 1st and 2nd row
    df = df.iloc[2:]
    # reset index
    df = df.reset_index(drop=True)

    # df.set_index(df.columns(0), inplace=True)
    # remove the 1st header
    df.columns = df.columns.droplevel(0)

    df_stack = df.stack()

    df_index = df[df.columns[0]]

    # create a new column named indicador in df_stack, where its string comes from the correponding value that corresponds the index of df_index and df_stack
    df_stack["Indicador"] = df_index[df_stack.index.get_level_values(0)].values

    df_stack.reset_index(inplace=True)

    # make sure that colum utentes cumprideos and total utentes is an integer, and substitute . with , in thousands
    df_stack["Utentes Cumpridores"] = df_stack["Utentes Cumpridores"].str.replace(
        ".", ""
    )
    df_stack["Total Utentes"] = df_stack["Total Utentes"].str.replace(".", "")

    df_stack["Utentes Cumpridores"] = df_stack["Utentes Cumpridores"].astype(int)
    df_stack["Total Utentes"] = df_stack["Total Utentes"].astype(int)

    # create a new column thatb results from the percentage of indicador cumpridor and total
    df_stack["CUMPRIMENTO"] = (
        df_stack["Utentes Cumpridores"] / df_stack["Total Utentes"] * 100
    )

    # round the column cumprimento to 0 decimal places
    df_stack["CUMPRIMENTO"] = df_stack["CUMPRIMENTO"].round(1)

    # rename the column level_1 to Medico Familia
    df_stack = df_stack.rename(columns={"level_1": "Medico Familia"})

    df_stack = normalizacao_medico_familia(df_stack)

    df_final = df_stack[
        [
            "Indicador",
            "Medico Familia",
            "Total Utentes",
            "Utentes Cumpridores",
            "CUMPRIMENTO",
        ]
    ]
    df_final["id"] = df_final["Indicador"].apply(id_indicador)

    df_final.dropna(inplace=True)

    intervalos = pd.read_csv("data/indicadores_post_processed.csv")

    df_com_intervalos = pd.merge(df_final, intervalos, how="left", on="id")
    # .drop_duplicates()

    df_com_intervalos.dropna(inplace=True)

    # create new rows with the weighted average of the cumprimento for each indicador
    df_com_intervalos = cumprimento_unidade(df_com_intervalos)

    df_com_intervalos = df_com_intervalos[
        [
            "id",
            "nome_abreviado",
            "area_clinica",
            "Medico Familia",
            "Total Utentes",
            "Utentes Cumpridores",
            "CUMPRIMENTO",
            "min_aceitavel",
            "min_esperado",
            "max_esperado",
            "max_aceitavel",
        ]
    ]

    # sort dataframe by id in ascending order
    df_com_intervalos.sort_values(by=["id"], inplace=True)

    return df_com_intervalos


def etl_xlsx(file_xlsx):
    if file_xlsx is not None:
        # file_xlsx = pd.read_excel(file_xlsx, engine="openpyxl")
        file_xlsx = pd.read_excel(file_xlsx)

    else:
        file_xlsx = pd.read_excel(
            "/data/P02_01_R04_ Indicadores por lista de utentes de médico - cumpridores e não cumpridores.xlsx"
        )

    df = preprocess(file_xlsx)
    return df


def etl_bicsp(file):
    df_bicsp = pd.read_excel(file, engine="openpyxl")

    # make the df_bicsp row 1 the header and remove the current header and the row 0
    df_bicsp.columns = df_bicsp.iloc[1]

    df_bicsp = df_bicsp.drop(df_bicsp.index[0:2])

    df_bicsp = df_bicsp.reset_index(drop=True)

    df_bicsp = extrair_indicadores(df_bicsp, "Cód. Indicador")

    df_bicsp = df_bicsp.rename({"Cód. Indicador": "id"}, axis=1)
    df_bicsp["id"] = df_bicsp["id"].astype(int)

    # remover colunas
    df_bicsp = df_bicsp.drop(
        ["Usado no IDG Nacional (S/N)", "Mês Ind", "Exclusão"], axis=1
    )

    # import a csv with the scores arlready calculated
    df_score = pd.read_csv("data/df_sunburst_pre_graph.csv")
    df_score = df_score[["id_indicador", "value"]]

    # rename id_indicador to id
    df_score = df_score.rename(columns={"id_indicador": "id", "value": "percentagem"})

    # merge the 2 dataframes so that df gets a new column where the ID is the same
    df_bicsp = pd.merge(df_bicsp, df_score, how="left", on="id")

    df_bicsp["percentagem_final"] = df_bicsp["percentagem"] * df_bicsp["Score"] / 2

    # reduce the number of columns
    df_bicsp = df_bicsp.drop(["Tipo "], axis=1)

    # change name of column
    df_bicsp = df_bicsp.rename(
        columns={
            "Designação Indicador (+ID)": "Nome Indicador",
            "percentagem": "percentagem_do_idg",
            "Hierarquia Contratual - Área": "Área",
            "Hierarquia Contratual - Sub-Área": "Sub-Área",
            "Hierarquia Contratual - Dimensão": "Dimensão",
        }
    )

    # filtrar apenas aqueles que são S na coluna IDG
    df_bicsp = df_bicsp[df_bicsp[" IDG"] == "S"]

    # remover a coluna IDG
    df_bicsp = df_bicsp.drop([" IDG"], axis=1)

    # sort dataframe by id in ascending order
    df_bicsp.sort_values(by=["id"], inplace=True)
    # reset index
    df_bicsp.reset_index(drop=True, inplace=True)

    # remove index column

    return df_bicsp
