import os
from typing import List
from TARAVisualize import pd
from TARAVisualize import st


def download_selected_mag_data(dataframes: List[pd.DataFrame]):
    """ Download all MAGs from filtered data into single tsv file

    :param dataframes: List of pandas dataframes to write
    """
    if st.sidebar.button("Download selection data"):
        out = pd.DataFrame()
        out_file = os.path.join(os.getcwd(), 'out.tsv')
        for df in dataframes:
            out = out.join(df, how="outer")
        out.to_csv(out_file, sep="\t")
        st.sidebar.text(f"Saved to {out_file}")
