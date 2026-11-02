import yaml
from src.ingestion.ingestion import load_orders
from src.features.features import build_daily_revenue
from src.detection.detection import detect_anomalies
from src.reporting.report import add_deviation, plot_revenue, write_report


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
    result_deviation = add_deviation(results=result)
    plot_revenue(results=result_deviation, output_path=config["paths"]["report_chart"])
    write_report(
        results=result_deviation,
        chart_path=config["paths"]["report_chart"],
        output_path=config["paths"]["report"],
        window=config["detection"]["rolling_window"],
        threshold=config["detection"]["z_threshold"],
    )
    result.to_csv(path_or_buf=config["paths"]["detection_results"], index=False)
    print(f"{len(result)} gün işlendi, {result['is_anomaly'].sum()} anomali bulundu.")


if __name__ == "__main__":
    main()
