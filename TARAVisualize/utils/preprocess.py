from sklearn import preprocessing
from TARAVisualize import pd


def fix(df):
    df = df.loc[:, (df != 0).any(axis=0)]
    x = df.values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    return pd.DataFrame(x_scaled, columns=df.columns, index=df.index)
