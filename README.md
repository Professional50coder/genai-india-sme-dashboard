# 🚀 GenAI India SME — Market Entry Intelligence Dashboard

> **Interactive Streamlit dashboard** for the *Market Entry Strategy: Generative AI SaaS for Indian SMEs* consulting project. Features real-time data sync, interactive slide navigation, live KPI monitoring, and full financial model visualizations.

---

## 📸 What's Inside

| Slide / Section | What It Shows |
|---|---|
| 📊 **Overview** | Macro market stats, India AI growth trajectory, project scope |
| 🌏 **Market Sizing** | TAM / SAM / SOM with nested circle viz + city-tier breakdown |
| ⚔️ **Competitors** | Bubble chart (30+ players) + detailed benchmarking table |
| 🔬 **Five Forces** | Radar chart + per-force analysis with threat ratings |
| 💬 **Customer Insights** | Survey results (n=42), use case demand ranking, key findings |
| 💹 **Financial Model** | ARR projections, funnel chart, unit economics, scenario analysis |
| 🚀 **Go-to-Market** | 3-phase roadmap, pricing tiers, GTM channels |
| 📡 **Live Dashboard** | Real-time SME count, MRR ticker, activity feed, city breakdown |

---

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.9 or higher
- pip

### 2. Clone / Download

```bash
git clone https://github.com/your-org/genai-india-sme-dashboard.git
cd genai-india-sme-dashboard
```

Or just drop `app.py` and `requirements.txt` in a folder.

### 3. Create a Virtual Environment (recommended)

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the App

```bash
streamlit run app.py
```

The dashboard will open in your browser at **http://localhost:8501**

---

## 📦 requirements.txt

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
numpy>=1.24.0
```

> No external API keys needed. The live dashboard simulates real-time data using `numpy.random` and Streamlit's session state.

---

## 🗂️ Project Structure

```
genai-india-sme-dashboard/
│
├── app.py                  ← Main Streamlit application (single file)
├── requirements.txt        ← Python dependencies
└── README.md               ← You are here
```

### Optional: Multi-page structure

If you want to split slides into separate files, Streamlit supports multi-page apps:

```
genai-india-sme-dashboard/
│
├── app.py                  ← Entry point (Overview page)
├── requirements.txt
├── README.md
└── pages/
    ├── 1_Market_Sizing.py
    ├── 2_Competitors.py
    ├── 3_Five_Forces.py
    ├── 4_Customer_Insights.py
    ├── 5_Financial_Model.py
    ├── 6_GoToMarket.py
    └── 7_Live_Dashboard.py
```

---

## 🔴 Live Data Sync

The **📡 Live Dashboard** slide simulates real-time data ingestion.

### How it works

| Feature | Mechanism |
|---|---|
| Live toggle | `st.toggle` + `st.session_state.auto_refresh` |
| Auto-refresh | `time.sleep(N)` → `st.rerun()` in a loop |
| State persistence | All metrics stored in `st.session_state` |
| Sparklines | Rolling 30-point history arrays (MRR, SME count) |
| Manual refresh | ⟳ button in sidebar triggers `tick_live_data()` |

### Connecting Real Data

To replace simulation with real data, swap `tick_live_data()` with your actual data source:

```python
# Example: pull from a PostgreSQL DB
import psycopg2

def tick_live_data():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM active_subscriptions;")
    st.session_state.live_smes = cursor.fetchone()[0]
    conn.close()
```

Or from a REST API:

```python
import requests

def tick_live_data():
    resp = requests.get("https://your-api.com/metrics/live")
    data = resp.json()
    st.session_state.live_smes = data["active_smes"]
    st.session_state.live_mrr  = data["mrr_inr"]
```

Or from Google Sheets (live market research data):

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_survey_data():
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("SME Survey Data").sheet1
    return pd.DataFrame(sheet.get_all_records())
```

---

## 🎨 Design System

The dashboard uses a custom dark theme with CSS injected via `st.markdown`:

| Token | Color | Usage |
|---|---|---|
| `--navy` | `#0D1B2A` | Background |
| `--teal` | `#1A6B8A` | Primary accent |
| `--mint` | `#00C4A7` | Highlight / values |
| `--sky`  | `#4FC3F7` | Secondary accent |
| `--gold` | `#F59E0B` | Warnings / medium risk |
| `--red`  | `#EF4444` | High risk / churn |
| `--green`| `#22C55E` | Positive / low risk |

Font: [DM Sans](https://fonts.google.com/specimen/DM+Sans) (loaded via Google Fonts CDN)

---

## 📊 Data Sources

All market data in this dashboard is based on:

| Source | Used For |
|---|---|
| MSME Ministry Annual Report 2024 | SME count, registration data |
| NASSCOM AI Landscape Report 2025 | Market sizing, CAGR, AI adoption |
| IDC India Cloud & AI Forecast 2025 | TAM/SAM methodology |
| McKinsey India SME AI Adoption Study | Willingness to pay, use cases |
| Primary Survey (n=42 SMEs) | Customer insights, feature demand |
| TRAI Annual Report 2024 | Internet/smartphone penetration |
| Tracxn / Crunchbase | Competitor funding & pricing |

---

## 🚀 Deployment

### Streamlit Community Cloud (Free)

1. Push `app.py` + `requirements.txt` to a public GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo → Deploy in 2 minutes

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t genai-sme-dashboard .
docker run -p 8501:8501 genai-sme-dashboard
```

### Railway / Render / Fly.io

Use the Dockerfile above. All three platforms auto-detect and deploy from GitHub.

---

## 🔧 Customization

### Change refresh interval

In the sidebar, use the **"Refresh interval (sec)"** slider (1–10 seconds).

### Add a new slide/section

1. Add your label to the `slides` list in the sidebar section:
```python
slides = [
    ...
    ("📌", "My New Slide"),
]
```

2. Add a matching `elif` block in the slide rendering section:
```python
elif active == "📌 My New Slide":
    slide_header("My New Slide", "Subtitle goes here")
    # Your content here
```

### Swap in real financial data

Replace the hardcoded arrays (e.g., `arr = [2, 5, 11, 20, ...]`) with a `pd.read_csv()` or database query.

---

## 📄 Resume Bullet Points (Reference)

> Use these when adding this project to your resume:

- Built an **interactive Streamlit market intelligence dashboard** for GenAI SaaS targeting Indian SMEs, featuring real-time data sync, 8 slide sections, and live KPI monitoring with Plotly visualizations
- Conducted market sizing analysis estimating a **$18.5B TAM** and $4.5B SAM, with bottom-up modeling across 63M+ Indian SMEs
- Analyzed 30+ competitors across 4 segments using Porter's Five Forces and a 8-dimension benchmarking matrix
- Modeled a **₹253Cr ARR Year 3 target** with LTV:CAC of 7.7x, break-even at Month 18, using a freemium-to-paid conversion funnel

---

## 📝 License

This project is for educational and portfolio purposes. Market data is estimated and should not be used for investment decisions without independent verification.

---

*Prepared by the Strategy & Market Intelligence Team · March 2026*
