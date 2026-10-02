# Anomali Tasarımı

## Amaç
Olist günlük verisinde kritik e-ticaret KPI'larındaki
anomalileri otomatik tespit edip nedenini ve iş etkisini
Türkçe özetleyen bir sistem. Kullanıcı: her sabah
"dün ne oldu?" sorusunu soran operasyon/analitik ekibi.

## KPI Listesi
| KPI | Yakaladığı anomali |
|---|---|
| Günlük gelir | Genel sağlık |
| Sipariş sayısı (ödeme tipine göre) | 2: Ödeme kesintisi |
| ASP (kategori bazında) | 1: Fiyat hatası |
| AOV, basket size | 1 (destekleyici) |
| Ortalama teslimat süresi | 3: Kargo |
| Ortalama review_score | 3 (destekleyici) |

## Anomali 1: Fiyat Hatası
- **Ne oluyor:** Bir kategoride sistem veya giriş hatasıyla
  fiyatlar normalin çok altına düşer.
- **İş problemi / ekip:** Zararına satış, iptal yükü,
  müşteri memnuniyeti kaybı. Pricing, Kategori Yönetimi.
- **Olist'te iz:** order_items.price düşer, sipariş sayısı artar.
- **İzleyen KPI:** Kategori bazında ASP (ana); AOV, basket size.
- **Enjeksiyon fikri:** Seçilen kategoride 1–2 gün boyunca
  fiyatları düşür, sipariş sayısını artır.
- **Not:** Gelir tek başına yetmez. Fiyat düşüşü hacim
  artışıyla dengelenebilir ya da küçük kategori toplamda
  kaybolur. Bu yüzden ASP şart.

## Anomali 2: Ödeme Kesintisi
- **Ne oluyor:** Bir ödeme altyapısı çöker, kredi kartıyla
  ödeme yapılamaz.
- **İş problemi / ekip:** Doğrudan gelir kaybı, müşteri
  rakibe gider. Payment, DevOps/SRE.
- **Olist'te iz:** payment_type = 'credit_card' siparişleri azalır.
- **İzleyen KPI:** Ödeme tipine göre günlük sipariş sayısı.
- **Enjeksiyon fikri:** 1–2 günde credit_card siparişlerinin
  bir kısmını veriden sil.
- **Not:** Olist'te başarısız ödeme, site trafiği ve ödeme
  timestamp'i yok. Conversion ölçülemez; sistem günlük çalışır.

## Anomali 3: Kargo Gecikmesi
- **Ne oluyor:** Kargo firmasının dağıtım merkezinde sorun
  çıkar, paketler günlerce gecikir.
- **İş problemi / ekip:** Müşteri mağduriyeti, çağrı merkezi
  yükü, NPS düşüşü. Lojistik, Müşteri Deneyimi (CX).
- **Olist'te iz:** order_delivered_customer_date ile
  order_delivered_carrier_date arası açılır; review_score düşer.
- **İzleyen KPI:** Ortalama teslimat süresi (ana);
  ortalama review_score (destekleyici).
- **Enjeksiyon fikri:** Seçilen dönemde teslim tarihlerini
  ileri kaydır, ilgili siparişlerin skorlarını düşür.
- **Not:** Yorumlar Portekizce, metin analizi yok, sadece
  skor kullanılır.

## Açık Kararlar
- Kargo anomalisi 24 Kasım 2017 Black Friday'in üstüne mi
  enjekte edilecek, sakin bir döneme mi? → Sakin dönem, ölçüm temiz olsun diye. Black Friday sonra zor test olarak.
- Verinin seyrek başı/sonu nereden kırpılacak? → Faz 1