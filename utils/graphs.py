import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def graph_indicador(df):
    (
        id_indicador,
        nome_indicador,
        min_aceitavel,
        min_esperado,
        max_esperado,
        max_aceitavel,
    ) = [
        df["id"],
        df["nome_indicador"],
        df["min_aceitavel"],
        df["min_esperado"],
        df["max_esperado"],
        df["max_aceitavel"],
    ]
    score = df["CUMPRIMENTO"]

    # Define the colors
    colors = ["red", "yellow", "green", "yellow", "red"]

    # Define the ranges of the colors
    ranges = [
        (0, min_aceitavel),
        (min_aceitavel, min_esperado),
        (min_esperado, max_esperado),
        (max_esperado, max_aceitavel),
        (max_aceitavel, 100),
    ]

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(5, 0.75))

    # Add the background areas
    for color, (start, end) in zip(colors, ranges):
        ax.axvspan(start, end, facecolor=color, alpha=0.3)

    # Plot the indicator value
    bar = ax.barh(id, score, height=0.6, color=(46 / 255, 80 / 255, 140 / 255, 1))

    # Set the plot limits and ticks
    ax.set_xlim(0, 100)
    ax.set_ylim(id - 0.5, id + 0.5)
    ax.set_yticks([])
    ax.set_xticks([min_aceitavel, min_esperado, max_esperado, max_aceitavel])

    # Set the y-label and title
    ax.set_title(f"{id_indicador} - {nome_indicador}")

    # Add the value label
    rect = bar[0]
    width = rect.get_width()
    ax.text(
        width, rect.get_y() + rect.get_height() / 2, f"{width}%", ha="left", va="center"
    )

    # Display the plot in Streamlit
    return st.pyplot(fig)


def sunburst(df):

    """lista_areas = df["Área"].unique().tolist()
    score_areas = {}
    for each in lista_areas:
        df_area = df[df["Área"] == each]

        # get the sum of all values where the "area" is Desempneho assistencial
        desempenho = df_area[df_area["Área"] == "Desempenho assistencial"][
            "Percentagem"
        ].sum()
        desempenho_maximo = df_area[df_area["Área"] == "Desempenho assistencial"][
            "Percentagem do IDG"
        ].sum()

        # append to a dict
        score_areas[each] = [desempenho, desempenho_maximo]"""

def bar_chart(df):

    """
    Create a pie chart where the size of each pie is the percentage_do_idg and the color and label of each pie comes from the score of its idicadores
    """

    list_areas = df["Área"].unique().tolist()
    df_pie_chart = pd.DataFrame()
    
    for each in list_areas:
        
        #sumatório da percentagem do idg
        percentagem_do_idg = df[df["Área"] == each]["percentagem_do_idg"].sum()

        #sumatório da percentagem final
        percentagem_final = df[df["Área"] == each]["percentagem_final"].sum()

        dict_to_df = {"Área": each, "percentagem_do_idg": percentagem_do_idg, "percentagem_final": percentagem_final}

        #append to a dataframe
        df_pie_chart = df_pie_chart.append(dict_to_df, ignore_index=True)

    # append to df_pie_chart a last parameter to make sum of percentagem do idg 100
    df_pie_chart = df_pie_chart.append(
        {"Área": "Sem Indicadores", "percentagem_do_idg": 100-68.8, "percentagem_final": 100-68.8},
        ignore_index=True,
    )

    #nova coluna com percentagem de completo
    df_pie_chart["percentagem"] = df_pie_chart["percentagem_final"] / df_pie_chart["percentagem_do_idg"]

    df_pie_chart["diference"] = df_pie_chart["percentagem_final"] - df_pie_chart["percentagem_do_idg"]

    #rgb colors for each area from a RdYlGr gradient depending on the value of percentagem in between 0 a 1
    df_pie_chart["color"] = df_pie_chart["percentagem"].apply(lambda x: plt.cm.RdYlGn(x))



    """# stacked vertical bar  chart for each area, where percentagem_final corresponds to 
    fig, ax = plt.subplots(figsize=(5,5))
    ax.bar(
        x = df_pie_chart["Área"],
        height = df_pie_chart["percentagem_final"],
        color = df_pie_chart["color"],
        label = df_pie_chart["Área"]
    )"""


    """# pie chart
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(
        x =df_pie_chart["percentagem_do_idg"],
        labels = df_pie_chart["Área"],
        colors = df_pie_chart["color"],

    )"""
    
    return df_pie_chart
    #return st.pyplot(fig)
    
    