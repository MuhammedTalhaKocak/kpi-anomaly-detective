import numpy as np
import pandas as pd


def mad_hesapla(degerler: np.ndarray) -> float:
    median = np.median(degerler)
    mutlak_farklar = np.abs(degerler - median)
    farklarin_mediani = np.median(mutlak_farklar)
    return farklarin_mediani


def detect_anomalies(
    daily: pd.DataFrame, window: int, threshold: float
) -> pd.DataFrame:
    daily = daily.copy()
    gecmis = daily["revenue"].shift(1)
    daily["rolling_median"] = gecmis.rolling(window=window).median()
    daily["rolling_mad"] = gecmis.rolling(window=window).apply(
        func=mad_hesapla, raw=True
    )
    daily["robust_zscore"] = (
        0.6745 * (daily["revenue"] - daily["rolling_median"]) / daily["rolling_mad"]
    )
    mask = abs(daily["robust_zscore"]) > threshold
    daily["is_anomaly"] = mask
    return daily
