import matplotlib.pyplot as plt
import streamlit as st


def graph_indicador(df):
    id, nome, min_aceitavel, min_esperado, max_esperado, max_aceitavel = [
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
    ax.set_title(f"{id} - {nome}")

    # Add the value label
    rect = bar[0]
    width = rect.get_width()
    ax.text(
        width, rect.get_y() + rect.get_height() / 2, f"{width}%", ha="left", va="center"
    )

    # Display the plot in Streamlit
    return st.pyplot(fig)
