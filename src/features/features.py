import pandas as pd


def build_daily_revenue(orders: pd.DataFrame) -> pd.DataFrame:
    daily_revenue = orders.groupby(orders["order_purchase_timestamp"].dt.normalize())[
        "price"
    ].sum()
    daily_revenue = daily_revenue.asfreq("D", fill_value=0)
    df = daily_revenue.to_frame().reset_index()
    df.columns = ["date", "revenue"]
    return df
