def cumprimento_unidade(df):
    list_indicadores = df["id"].unique().tolist()

    for each in list_indicadores:
        df_indicador = df[df["id"] == each]

        df_indicador = df_indicador.groupby(
            ["nome_abreviado", "id", "min_aceitavel", "min_esperado", "max_esperado", "max_aceitavel", "area_clinica"]
        ).agg(
            {"Total Utentes": "sum", "Utentes Cumpridores": "sum"}
        ).reset_index()
        df_indicador["CUMPRIMENTO"] = (df_indicador["Utentes Cumpridores"] / df_indicador["Total Utentes"] * 100).round(1)
        df_indicador["Medico Familia"] = "Unidade"

        df = df.append(df_indicador)

    return df