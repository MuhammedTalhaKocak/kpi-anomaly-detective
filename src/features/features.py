import pandas as pd


def build_daily_revenue(orders: pd.DataFrame, metric: dict) -> pd.DataFrame:
    daily_revenue = orders.groupby(orders[metric["date_column"]].dt.normalize())[
        metric["value_column"]
    ].sum()
    daily_revenue = daily_revenue.asfreq("D", fill_value=0)
    df = daily_revenue.to_frame().reset_index()
    df.columns = ["date", "revenue"]
    return df
