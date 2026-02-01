# 📰 OLC - Open Learn Close

> Haber okumayı yeniden tasarla: Aç, Öğren, Kapat!

[![Demo](https://img.shields.io/badge/🚀_Live_Demo-bit.ly/olc--haber-2ecc71?style=for-the-badge)](https://bit.ly/olc-haber)
[![GitHub](https://img.shields.io/badge/GitHub-S9--gif-24292e?style=for-the-badge&logo=github)](https://github.com/S9-gif/OLC-My-First-Project)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge)](https://olc-backend.onrender.com/docs)

---

## 🎯 Proje Hakkında

OLC (Open Learn Close), spor, kitap, teknoloji, borsa vb... kategorilerinde haberleri otomatik toplayan, AI ile özetleyen ve 3 seviyeli okuma deneyimi sunan akıllı haber platformudur.

**Felsefe:** Uzun haberleri okumak ve ham bilgiyi öğrenmek için saatler harcamak yerine, AI özetleri ile 30 saniyede öğren!

---

## 📰 OLC 3 Seviyeli Okuma Sistemi

| Seviye | Süre | Ne Göster |
|--------|------|-----------|
| 📰 **OPEN** | 5 saniye | Flash özet — 2 cümle |
| 📚 **LEARN** | 30 saniye | Detaylı özet — Bullet points |
| 📄 **CLOSE** | 2 dakika | Tam metin + kaynak link |

---

## ✨ Özellikler

- 🤖 **AI Özet** — GPT-4o-mini ile otomatik flash + detaylı özet
- 📊 **Sentiment Analizi** — Haberin genel havası (olumlu / nötr / olumsuz)
- 🔥 **Trend Takibi** — En çok konuşulan konular ve anahtar kelimeler
- 🎯 **Filtreleme** — Kategori, sentiment ve arama ile kolay erişim
- 📈 **Dashboard** — Interaktif grafiklere sahip analitik sayfa
- ⚡ **Otomatik Toplama** — N8N ile her 6 saatte yeni haberler

---

## �moderna️ Teknoloji Stack'i

```
Backend:
├── Python 3
├── FastAPI          → REST API
├── SQLAlchemy       → ORM
├── PostgreSQL       → Database
└── OpenAI GPT-4o-mini → AI özet + sentiment

Frontend:
├── Streamlit        → Web UI
├── Plotly           → Interaktif grafikler
└── Pandas           → Data processing

Automation:
└── N8N              → RSS → API otomasyonu

Deployment:
├── Render           → Backend + Database
└── Streamlit Cloud  → Frontend
```

---

## 🏗️ Sistem Mimarisi

```
┌──────────┐    RSS     ┌───────┐   POST   ┌─────────┐
│  N8N     │──────────→ │ N8N   │─────────→│ Backend │
│ Schedule │            │ Parse │          │ (Render)│
└──────────┘            └───────┘          └────┬────┘
                                                │
                                          ┌─────▼─────┐
                                          │PostgreSQL │
                                          │  Database │
                                          └─────▲─────┘
                                                │
                                          ┌─────┴─────┐
                                          │ Streamlit │
                                          │  Frontend │
                                          └───────────┘
```

---

## 📡 API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/haberler` | Haber listesi (filtreli, sayfalı) |
| POST | `/api/v1/haberler` | Yeni haber ekle |
| GET | `/api/v1/haberler/{id}` | Tek haber |
| POST | `/api/v1/ai/process/{id}` | AI ile haber işle |
| POST | `/api/v1/ai/batch-process` | Toplu AI işleme |
| GET | `/api/v1/stats/sentiment` | Sentiment istatistikleri |

📄 **Swagger Docs:** [olc-backend.onrender.com/docs](https://olc-backend.onrender.com/docs)

---

## 📅 Geliştirme Durumu

| Adım | Durum |
|------|-------|
| Database & Models | ✅ Tamamlandı |
| REST API Endpoints | ✅ Tamamlandı |
| AI Entegrasyonu | ✅ Tamamlandı |
| N8N Otomasyonu | ✅ Tamamlandı |
| Streamlit Frontend | ✅ Tamamlandı |
| Deployment | ✅ Tamamlandı |

---

## 📖 Geliştirme Günlüğü

https://www.notion.so/wwwsercankuru/lk-proje-denemem-OLC-Open-Learn-Close-2e59e0171b448031ab8ae4cd54ca88e3

---

## 👤 Geliştirici

**Ahmet Sercan Kuru**
Gazi Üniversitesi — İstatistik Bölümü

---

> **"Open it. Learn it. Close it. Move on."**

## 📄 Lisans

MIT
