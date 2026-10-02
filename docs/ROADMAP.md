# ROADMAP

> Kapsam testi: "Bu, dün ne oldu / neden oldu /
> kaça mal oldu sorusunu daha iyi cevaplıyor mu?"
> Hayırsa → "Sonra" bölümüne.

## Faz 0 — İş Çerçevesi ✅
- Veri kaynağı: Olist
- Anomali tipleri ve KPI listesi → docs/anomaly_design.md

## Faz 1 — En Basit Uçtan Uca
- Tek KPI: günlük gelir
- Basit z-score tespiti
- pipeline.py script olarak, çıktı: rapor
- configs/metrics.yaml (metric layer, hafif)

## Faz 2 — Gerçekçilik ve Ölçüm
- Günlük replay
- Anomali enjeksiyonu + ground truth
- Veri kalitesi kontrolleri (data contracts)
- Precision / recall ölçümü
- Forecast tabanlı tespit

## Faz 3 — Root Cause
- Segment bazlı contribution analysis
- İş etkisi hesabı (beklenen − gerçekleşen)

## Faz 4 — LLM Katmanı
- Structured JSON → Türkçe yönetici özeti
- Hallucination kontrolü
- LLM evaluation

## Faz 5 — Otomasyon ve Deploy
- GitHub Actions ile günlük çalışma
- Docker
- Dashboard + FastAPI endpoint

## Faz 6 — MLOps
- MLflow (experiment tracking, registry)
- CI kalite kapısı
- Drift monitoring

## Sonra (kapsam dışı)
- Agentic root cause (tool calling)
- Text-to-SQL
