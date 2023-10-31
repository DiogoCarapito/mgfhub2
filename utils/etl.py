"""
ETL pipeline for data processing
"""

import pandas as pd


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
    df_stack["Cumprimento"] = (
        df_stack["Utentes Cumpridores"] / df_stack["Total Utentes"] * 100
    )

    # round the column cumprimento to 0 decimal places
    df_stack["Cumprimento"] = df_stack["Cumprimento"].round(1)

    # rename the column level_1 to Medico Familia
    df_stack = df_stack.rename(columns={"level_1": "Medico Familia"})

    # the column medico familia sould have upper case only in the first letter of each word and remove all the spaces expect between the words
    df_stack["Medico Familia"] = df_stack["Medico Familia"].str.title()

    # remove the double spaces in the string
    df_stack["Medico Familia"] = df_stack["Medico Familia"].str.replace("  ", " ")

    # remove the last space in the string
    df_stack["Medico Familia"] = df_stack["Medico Familia"].str.rstrip()

    df_final = df_stack[["Indicador", "Medico Familia", "Total Utentes", "Cumprimento"]]

    return df_final


def etl_xlsx(file_xlsx):
    if file_xlsx is not None:
        # file_xlsx = pd.read_excel(file_xlsx, engine="openpyxl")
        file_xlsx = pd.read_excel(file_xlsx)

        # preprocess
    else:
        try:
            file_xlsx = pd.read_excel(
                "data/P02_01_R04_ Indicadores por lista de utentes de médico - cumpridores e não cumpridores.xlsx"
            )
        except:
            return None

    df = preprocess(file_xlsx)
    return df
