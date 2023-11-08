def func():
    return None

def normalizacao_medico_familia(df):
    # the column medico familia sould have upper case only in the first letter of each word and remove all the spaces expect between the words
    df["Medico Familia"] = df["Medico Familia"].str.title()

    # remove the double spaces in the string
    df["Medico Familia"] = df["Medico Familia"].str.replace("  ", " ")

    # remove the last space in the string
    df["Medico Familia"] = df["Medico Familia"].str.rstrip()

    return df


def transform_to_float(df, columns):
    for column in columns:
        df[column] = df[column].str.replace(".", "")
        df[column] = df[column].str.replace(",", ".")
        df[column] = df[column].astype(float)
    return df
