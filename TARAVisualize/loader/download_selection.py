import base64
import os
from typing import List
from TARAVisualize import pd
from TARAVisualize import st


# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/2
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href


def download_selected_mag_data(dataframes: List[pd.DataFrame]):
    """ Download all MAGs from filtered data into single tsv file

    :param dataframes: List of pandas dataframes to write
    """
    if st.sidebar.button("Download selection data"):
        out = pd.DataFrame()
        st.sidebar.text(f"Collecting data")
        for df in dataframes:
            out = out.join(df, how="outer")
        st.markdown(get_table_download_link(out), unsafe_allow_html=True)
        # out.to_csv(out_file, sep="\t")
        # st.sidebar.text(f"Saved to {out_file}")
        st.sidebar.text("Saved!")
