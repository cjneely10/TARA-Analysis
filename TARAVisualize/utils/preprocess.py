from TARAVisualize import pd


def fix(df):
    df = df.loc[:, (df != 0).any(axis=0)]
    df[df != 0] = 1
    return pd.DataFrame(df, columns=df.columns, index=df.index)
