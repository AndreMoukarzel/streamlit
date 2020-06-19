import base64

import streamlit as st
import pandas as pd


def get_download_link(df: pd.DataFrame) -> str:
    """Generates link to download the given Dataframe """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}">Download csv file<a/>'


def main():
    st.title('Dataset Analyser')
    
    csv_file = st.file_uploader("Upload your (.csv) dataset", type="csv")
    if csv_file is None:
        return
    df = pd.read_csv(csv_file)

    st.markdown("**Dataframe's Shape**")
    st.markdown(df.shape)

    st.markdown("**Found columns:**")
    st.write(list(df.columns))

    head_slider = st.slider("*Ammount of values presented*", min_value=1, max_value=df.shape[0],
                            value=min(10, df.shape[0]))
    st.dataframe(df.head(head_slider))

    data_types = pd.DataFrame({
        'names': df.columns,
        'types': df.dtypes,
        'NA #': df.isna().sum(),
        'NA %': 100 * df.isna().sum() / df.shape[0]
    })

    st.markdown("**Found " + str(len(data_types.types.unique())) + " different type(s) of data:**")
    st.table(data_types[['types']])

    st.subheader("Overwrite missing values")
    percent = st.slider("Choose the maximum ammount of missing data for columns to be considered",
                        min_value=0, max_value=100)
    cols = list(data_types[data_types['NA %'] <= percent]['names'])
    method = st.radio("Choose the measurement used:", ('Mean', 'Median'))
    if method == "Mean":
        df_inputed = df[cols].fillna(df[cols].mean())
    elif method == "Median":
        df_inputed = df[cols].fillna(df[cols].median())
    st.dataframe(df_inputed)
    #st.write(get_download_link(df_inputed), unsafe_allow_html=True)


if __name__ == "__main__":
    main()