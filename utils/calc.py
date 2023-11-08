
def calc_score(df):
    # calc score each row
    df["score"] = 0
    
    # if valor is between min_aceitavel and min_esperado, is equal to a normalized value between 0 and 2 depending how close it is to min_esperado and how far it is from min_aceitavel
    df.loc[
        (df["Valor"] >= df["min_aceitavel"]) & (df["Valor"] < df["min_esperado"]),
        "score",
    ] = (
        2
        - (
            (df["min_esperado"] - df["Valor"])
            / (df["min_esperado"] - df["min_aceitavel"])
        )
        * 2
    )

    # if valor is between min_esperado and max_esperado, is equal to 2
    df.loc[
        (df["Valor"] >= df["min_esperado"]) & (df["Valor"] <= df["max_esperado"]),
        "score",
    ] = 2

    # if valor is between max_esperado and max_aceitavel, is equal to a normalized value between 2 and 0 depending how close it is to max_esperado and how far it is from max_aceitavel
    df.loc[
        (df["Valor"] > df["max_esperado"]) & (df["Valor"] <= df["max_aceitavel"]),
        "score",
    ] = (
        2
        - (
            (df["Valor"] - df["max_esperado"])
            / (df["max_aceitavel"] - df["max_esperado"])
        )
        * 2
    )

    # if valor is greater than max_aceitavel, is equal to 0
    df.loc[df["Valor"] > df["max_aceitavel"], "score"] = 0

    # if valor is less than min_aceitavel, is equal to 0
    df.loc[df["Valor"] < df["min_aceitavel"], "score"] = 0

    #df["score"] = 2
    
    return df
        


def cumprimento_unidade(df):
    list_indicadores = df["id"].unique().tolist()

    for each in list_indicadores:
        df_indicador = df[df["id"] == each]

        df_indicador = (
            df_indicador.groupby(
                [
                    "nome_abreviado",
                    "id",
                    "min_aceitavel",
                    "min_esperado",
                    "max_esperado",
                    "max_aceitavel",
                    "area_clinica",
                ]
            )
            .agg({"Total Utentes": "sum", "Utentes Cumpridores": "sum"})
            .reset_index()
        )
        #df_indicador["Valor"] = 100
        df_indicador["Valor"] = (
            df_indicador["Utentes Cumpridores"] / df_indicador["Total Utentes"] * 100
        ).round(1)
        df_indicador["Medico Familia"] = "Unidade"

        df = df.append(df_indicador)

        df.sort_values(by=["id"], inplace=True)
        df.reset_index(drop=True, inplace=True)

    return df


def calcular_idg(df):
    #df = df[df["Hierarquia Contratual - Área"] == "Desempenho Assistencial"]
    return round(df["percentagem_final"].sum(), 2)

def calcular_idg_maximo(df):
    return round(df["percentagem_do_idg"].sum(), 2)