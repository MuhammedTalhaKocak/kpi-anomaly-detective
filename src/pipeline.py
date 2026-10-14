import yaml
from src.ingestion.ingestion import load_orders
from src.features.features import build_daily_revenue
from src.detection.detection import detect_anomalies


def main():
    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)
    with open("configs/metrics.yaml") as f:
        metrics = yaml.safe_load(f)
    revenue_def = metrics["revenue"]
    orders = load_orders(config, revenue_def)
    daily = build_daily_revenue(orders, revenue_def)
    daily.to_csv(path_or_buf=config["paths"]["daily_revenue"], index=False)
    window = config["detection"]["rolling_window"]
    threshold = config["detection"]["z_threshold"]
    result = detect_anomalies(daily, window, threshold)
    result.to_csv(path_or_buf=config["paths"]["detection_results"], index=False)
    print(f"{len(result)} gün işlendi, {result['is_anomaly'].sum()} anomali bulundu.")


if __name__ == "__main__":
    main()
