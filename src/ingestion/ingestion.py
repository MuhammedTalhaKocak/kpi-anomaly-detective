import pandas as pd


def load_orders(config: dict, metric: dict) -> pd.DataFrame:
    """Olist orders + order_items'ı okur, iş kurallarını uygular,
    gelir hesabına hazır sipariş-kalem tablosu döndürür."""
    date_col = metric["date_column"]
    paths = config["paths"]
    orders = pd.read_csv(paths["orders"], parse_dates=[date_col])
    order_items = pd.read_csv(
        paths["order_items"], usecols=["order_id", metric["value_column"]]
    )

    orders = orders[orders["order_status"].isin(metric["valid_statuses"])]

    gun = orders[date_col].dt.normalize()
    orders = orders[
        gun.between(config["data"]["start_date"], config["data"]["end_date"])
    ]

    return orders.merge(order_items, on="order_id", how="inner")
