import streamlit as st
from utils.etl import etl_xlsx


def main():
    """Main page content"""
    st.title("mgfhub 2.0")

    # File uploader
    file_xlsx = st.file_uploader(
        "Upload de excel proveniente do MIMUF",
        type="xlsx",
        accept_multiple_files=False,
        help="Ajuda",
    )

    # Transform file into dataframe
    main_df = etl_xlsx(file_xlsx)

    st.table(main_df)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
