import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def add_deviation(results: pd.DataFrame) -> pd.DataFrame:
    results = results.copy()
    results["sapma"] = results["revenue"] - results["rolling_median"]
    results["sapma_pct"] = (results["sapma"] / results["rolling_median"]) * 100
    return results


def plot_revenue(results: pd.DataFrame, output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        results["date"],
        results["revenue"],
        label="Gerçek Gelir Çizgisi",
    )

    ax.plot(
        results["date"],
        results["rolling_median"],
        label="Beklenen Gelir Çizgisi",
        linestyle="--",
    )
    anomaliler = results[results["is_anomaly"]]
    ax.scatter(
        anomaliler["date"],
        anomaliler["revenue"],
        color="red",
        label="Anomali",
        zorder=3,
    )
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Gelir (BRL)")
    ax.set_title("Gerçek Gelir - Beklenen Gelir - Anomaliler")
    ax.legend()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fname=output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_report(
    results: pd.DataFrame,
    chart_path: str,
    output_path: str,
    window: int,
    threshold: int,
) -> None:
    son = results.iloc[-1]
    durum = "🔴 Anomali" if son["is_anomaly"] else "🟢 Normal"

    bolum_1 = f"""## 1. Son Gün Özeti ({son['date']:%Y-%m-%d})

| Gösterge | Değer |
| --- | --- |
| Gerçek Gelir | {son['revenue']:,.0f} BRL | 
| Beklenen Gelir | {son['rolling_median']:,.0f} BRL|
| Sapma |{son['sapma']:+,.0f} BRL ({son['sapma_pct']:+.1f}%)|
| Durum| {durum} |
| Robust z | {son["robust_zscore"]:+.1f} (eşik ±{threshold})
"""
    grafik_adi = Path(chart_path).name

    bolum_2 = f"""
## 2. Gelir Trendi

![Gerçek ve beklenen gelir, anomaliler]({grafik_adi})
"""
    anomaliler = results[results["is_anomaly"]].sort_values(by="date", ascending=False)
    tablo = pd.DataFrame(
        {
            "Tarih": anomaliler["date"].dt.strftime("%Y-%m-%d"),
            "Gerçek Gelir (BRL)": anomaliler["revenue"].map(lambda x: f"{x:,.0f}"),
            "Beklenen Gelir (BRL)": anomaliler["rolling_median"].map(
                lambda x: f"{x:,.0f}"
            ),
            "Sapma (BRL)": anomaliler["sapma"].map(lambda x: f"{x:+,.0f}"),
            "Sapma (%)": anomaliler["sapma_pct"].map(lambda x: f"{x:+.1f}%"),
            "Robust z": anomaliler["robust_zscore"].map(lambda x: f"{x:+.1f}"),
        }
    )
    bolum_3 = f"""
## 3. Tespit Edilen Anomaliler ({len(anomaliler)} gün)

{tablo.to_markdown(index=False)}
"""
    yukari_gun = (anomaliler["sapma"] > 0).sum()
    asagi_gun = (anomaliler["sapma"] < 0).sum()
    yukari_sapma = anomaliler.loc[anomaliler["sapma"] > 0, "sapma"].sum()
    asagi_sapma = anomaliler.loc[anomaliler["sapma"] < 0, "sapma"].sum()
    bolum_4 = f"""
## 4. Toplam Etki

| Yön | Gün | Toplam Sapma (BRL) |
| --- | --- | --- |
| Beklenenin üstü | {yukari_gun} | {yukari_sapma:+,.0f} |
| Beklenenin altı | {asagi_gun} | {asagi_sapma:+,.0f} |
"""
    bolum_5 = f"""
## 5. Sınırlamalar

- **Isınma Dönemi:** İlk {window} gün için karşılaştırılacak geçmiş veri olmadığından değerlendirme yapılmaz.
- **Sezonsallık:** Beklenen gelir son {window} günün medyanıdır; haftanın günü etkisini bilmez.
- **Bilinen Olaylar:** Black Friday (Kasım 2017) gibi kampanya dönemleri anomali olarak işaretlenir ve tek bir olay için çok sayıda alarm üretir.
- **Neden?** Anomalinin kaynağı (kategori, bölge, ödeme tipi) bu sürümde analiz edilmez; Faz 3'te eklenecektir.
"""
    rapor = (
        "# Günlük KPI Anomali Raporu\n\n"
        + bolum_1
        + bolum_2
        + bolum_3
        + bolum_4
        + bolum_5
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(rapor, encoding="utf-8")
