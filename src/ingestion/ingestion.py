import pandas as pd


def load_orders(config: dict) -> pd.DataFrame:
    """Olist orders + order_items'ı okur, iş kurallarını uygular,
    gelir hesabına hazır sipariş-kalem tablosu döndürür."""
    paths = config["paths"]
    orders = pd.read_csv(paths["orders"], parse_dates=["order_purchase_timestamp"])
    order_items = pd.read_csv(paths["order_items"], usecols=["order_id", "price"])

    orders = orders[orders["order_status"].isin(config["valid_statuses"])]

    gun = orders["order_purchase_timestamp"].dt.normalize()
    orders = orders[
        gun.between(config["data"]["start_date"], config["data"]["end_date"])
    ]

    return orders.merge(order_items, on="order_id", how="inner")
