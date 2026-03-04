
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import time
import random
from datetime import datetime, timedelta

# ─── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="GenAI India SME — Market Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

  /* ── Root tokens ── */
  :root {
    --navy:   #0D1B2A;
    --teal:   #1A6B8A;
    --mint:   #00C4A7;
    --sky:    #4FC3F7;
    --light:  #EFF6FF;
    --white:  #FFFFFF;
    --muted:  #64748B;
    --lgray:  #E2E8F0;
    --gold:   #F59E0B;
    --red:    #EF4444;
    --green:  #22C55E;
    --card-bg:#0F2336;
    --border: #1E3A4F;
  }

  /* ── Global reset ── */
  html, body, .stApp { background: var(--navy) !important; color: var(--white) !important; font-family: 'DM Sans', sans-serif !important; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] { background: #070F1A !important; border-right: 1px solid var(--border); }
  [data-testid="stSidebar"] * { color: var(--white) !important; font-family: 'DM Sans', sans-serif !important; }
  [data-testid="stSidebarNav"] { display: none; }

  /* ── Headers ── */
  h1, h2, h3, h4 { font-family: 'DM Sans', sans-serif !important; color: var(--white) !important; }

  /* ── Metric cards ── */
  [data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
  }
  [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 0.08em; }
  [data-testid="stMetricValue"] { color: var(--mint) !important; font-size: 28px !important; font-weight: 700 !important; }
  [data-testid="stMetricDelta"] svg { display: none; }

  /* ── Buttons ── */
  .stButton > button {
    background: var(--card-bg) !important;
    color: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s;
  }
  .stButton > button:hover {
    border-color: var(--mint) !important;
    color: var(--mint) !important;
  }

  /* ── Active nav button ── */
  .nav-active > button {
    border-color: var(--mint) !important;
    color: var(--mint) !important;
    background: #0a2235 !important;
  }

  /* ── Selectbox / inputs ── */
  .stSelectbox > div > div, .stSlider { background: var(--card-bg) !important; }

  /* ── Tables ── */
  .stDataFrame { border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }

  /* ── Dividers ── */
  hr { border-color: var(--border) !important; }

  /* ── Plotly overrides ── */
  .js-plotly-plot .plotly { border-radius: 12px; overflow: hidden; }

  /* ── Custom cards ── */
  .kpi-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--mint), var(--teal));
  }
  .kpi-card .kpi-val { font-size: 32px; font-weight: 700; color: var(--mint); line-height: 1.1; }
  .kpi-card .kpi-lbl { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
  .kpi-card .kpi-delta { font-size: 13px; color: var(--green); margin-top: 6px; }

  /* ── Slide header ── */
  .slide-header {
    background: linear-gradient(135deg, var(--teal) 0%, var(--navy) 100%);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    border-left: 4px solid var(--mint);
  }
  .slide-header h2 { margin: 0 0 4px 0 !important; font-size: 24px !important; }
  .slide-header p { margin: 0; color: var(--sky); font-size: 14px; }

  /* ── Tag chips ── */
  .chip {
    display: inline-block;
    background: #1a3a4f;
    border: 1px solid var(--teal);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    color: var(--sky);
    margin: 2px;
  }

  /* ── Info block ── */
  .info-block {
    background: #0a2235;
    border-left: 3px solid var(--mint);
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 8px 0;
  }
  .info-block .ib-title { font-weight: 600; color: var(--white); font-size: 14px; margin-bottom: 4px; }
  .info-block .ib-val { font-size: 22px; font-weight: 700; color: var(--mint); }
  .info-block .ib-note { font-size: 12px; color: var(--muted); margin-top: 2px; }

  /* ── Live badge ── */
  .live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0f2e1a;
    border: 1px solid var(--green);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: var(--green);
    font-weight: 600;
  }
  .live-dot {
    width: 7px; height: 7px;
    background: var(--green);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  /* ── Force table bg ── */
  .force-table-row {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: var(--navy); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  /* ── Tab styling ── */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--card-bg) !important;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
  }
  .stTabs [aria-selected="true"] {
    background: var(--teal) !important;
    color: var(--white) !important;
  }

  /* ── Progress bar ── */
  .stProgress > div > div { background: var(--mint) !important; }
</style>
""", unsafe_allow_html=True)


# ─── COLOUR PALETTE (for Plotly) ──────────────────────────────────
NAV   = "#0D1B2A"
TEAL  = "#1A6B8A"
MINT  = "#00C4A7"
SKY   = "#4FC3F7"
GOLD  = "#F59E0B"
RED   = "#EF4444"
GREEN = "#22C55E"
MUTED = "#64748B"
CARD  = "#0F2336"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=CARD,
    plot_bgcolor=CARD,
    font=dict(family="DM Sans", color="#CBD5E1"),
    margin=dict(l=16, r=16, t=40, b=16),
)

# Reusable axis styles (apply per-chart explicitly)
AXIS  = dict(gridcolor="#1E3A4F", linecolor="#1E3A4F", zerolinecolor="#1E3A4F")
AXISQ = dict(gridcolor="#1E3A4F", linecolor="#1E3A4F", showticklabels=False)


# ─── SESSION STATE & LIVE DATA ────────────────────────────────────
if "live_smes"      not in st.session_state: st.session_state.live_smes      = 1847
if "live_mrr"       not in st.session_state: st.session_state.live_mrr       = 23_04_650
if "live_churn"     not in st.session_state: st.session_state.live_churn     = 4.5
if "live_nps"       not in st.session_state: st.session_state.live_nps       = 52
if "live_cac"       not in st.session_state: st.session_state.live_cac       = 3750
if "tick"           not in st.session_state: st.session_state.tick           = 0
if "auto_refresh"   not in st.session_state: st.session_state.auto_refresh   = False
if "active_slide"   not in st.session_state: st.session_state.active_slide   = "📊 Overview"
if "history_mrr"    not in st.session_state:
    base = 230_000
    st.session_state.history_mrr = [int(base * (1 + 0.07 * i + random.uniform(-0.02, 0.02))) for i in range(30)]
if "history_smes"   not in st.session_state:
    st.session_state.history_smes = [1600 + i * 10 + random.randint(-5, 5) for i in range(30)]
if "history_ts"     not in st.session_state:
    now = datetime.now()
    st.session_state.history_ts = [(now - timedelta(days=29-i)).strftime("%b %d") for i in range(30)]

def tick_live_data():
    st.session_state.tick += 1
    delta_smes = random.randint(-3, 12)
    st.session_state.live_smes = max(0, st.session_state.live_smes + delta_smes)
    st.session_state.history_smes = st.session_state.history_smes[1:] + [st.session_state.live_smes]

    delta_mrr = random.randint(-5000, 18000)
    st.session_state.live_mrr = max(0, st.session_state.live_mrr + delta_mrr)
    st.session_state.history_mrr = st.session_state.history_mrr[1:] + [st.session_state.live_mrr]

    now_str = datetime.now().strftime("%H:%M:%S")
    st.session_state.history_ts = st.session_state.history_ts[1:] + [now_str]

    st.session_state.live_churn  = round(max(1.0, st.session_state.live_churn + random.uniform(-0.05, 0.05)), 2)
    st.session_state.live_nps    = min(80, max(30, st.session_state.live_nps + random.randint(-1, 1)))
    st.session_state.live_cac    = max(2500, st.session_state.live_cac + random.randint(-30, 30))


# ─── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 12px 0;'>
      <div style='font-size:22px;font-weight:700;color:#00C4A7;'>🚀 GenAI India</div>
      <div style='font-size:12px;color:#64748B;margin-top:2px;'>Market Entry Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Live sync toggle
    live_col1, live_col2 = st.columns([2, 1])
    with live_col1:
        auto = st.toggle("Live Sync", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto
    with live_col2:
        if st.button("⟳", help="Manual refresh"):
            tick_live_data()
            st.rerun()

    if st.session_state.auto_refresh:
        st.markdown('<div class="live-badge"><div class="live-dot"></div>LIVE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12px;color:#64748B;">⏸ Paused</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:11px;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">Navigation</div>', unsafe_allow_html=True)

    slides = [
        ("📊", "Overview"),
        ("🌏", "Market Sizing"),
        ("⚔️",  "Competitors"),
        ("🔬", "Five Forces"),
        ("💬", "Customer Insights"),
        ("💹", "Financial Model"),
        ("🚀", "Go-to-Market"),
        ("📡", "Live Dashboard"),
    ]

    for icon, name in slides:
        label = f"{icon} {name}"
        is_active = st.session_state.active_slide == label
        css_class = "nav-active" if is_active else ""
        with st.container():
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(label, key=f"nav_{name}", use_container_width=True):
                st.session_state.active_slide = label
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Refresh interval
    refresh_sec = st.slider("Refresh interval (sec)", 1, 10, 3)
    st.markdown(f'<div style="font-size:11px;color:#64748B;">Tick #{st.session_state.tick} · {datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:11px;color:#64748B;">Strategy & Market Intelligence<br>© March 2026 · Confidential</div>', unsafe_allow_html=True)


# ─── AUTO REFRESH ─────────────────────────────────────────────────
if st.session_state.auto_refresh:
    tick_live_data()
    time.sleep(refresh_sec)
    st.rerun()


# ─── SHARED HELPERS ───────────────────────────────────────────────
def slide_header(title, subtitle=""):
    st.markdown(f"""
    <div class="slide-header">
      <h2>{title}</h2>
      {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def kpi_card(val, label, delta=""):
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-val">{val}</div>
      <div class="kpi-lbl">{label}</div>
      {"<div class='kpi-delta'>" + delta + "</div>" if delta else ""}
    </div>
    """, unsafe_allow_html=True)

def info_block(title, value, note=""):
    st.markdown(f"""
    <div class="info-block">
      <div class="ib-title">{title}</div>
      <div class="ib-val">{value}</div>
      {"<div class='ib-note'>" + note + "</div>" if note else ""}
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# SLIDES
# ═══════════════════════════════════════════════════════════════════
active = st.session_state.active_slide


# ──────────────────────────────────────────────────────────────────
# SLIDE 1: OVERVIEW
# ──────────────────────────────────────────────────────────────────
if active == "📊 Overview":
    slide_header("Market Entry Strategy", "Generative AI SaaS for Indian SMEs · March 2026")

    col1, col2, col3, col4 = st.columns(4)
    with col1:  kpi_card("$18.5B", "TAM by 2028", "↑ 38% CAGR")
    with col2:  kpi_card("$4.5B",  "SAM by 2028", "24% of TAM")
    with col3:  kpi_card("63M+",   "Indian SMEs",  "Only 2% AI-enabled")
    with col4:  kpi_card("$135M",  "SOM Year 3",   "45K paying SMEs")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown("#### 📈 India AI Market Growth Trajectory")
        years  = [2022, 2023, 2024, 2025, 2026, 2027, 2028, 2030]
        values = [2.8,  3.9,  6.0,  8.3,  11.5, 15.0, 19.0, 29.0]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=years, y=values,
            marker=dict(color=MINT, opacity=0.85, line=dict(width=0)),
            text=[f"${v}B" for v in values],
            textposition="outside",
            textfont=dict(color="#CBD5E1", size=11),
        ))
        fig.add_trace(go.Scatter(
            x=years, y=values,
            mode="lines+markers",
            line=dict(color=SKY, width=2, dash="dot"),
            marker=dict(color=SKY, size=7),
            showlegend=False,
        ))
        fig.update_layout(**PLOTLY_LAYOUT,
            title=dict(text="India AI Market Size (USD Billion)", font=dict(color="#CBD5E1", size=13)),
            xaxis=dict(tickvals=years, gridcolor="#1E3A4F"),
            yaxis=dict(title="USD Billion", gridcolor="#1E3A4F"),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### 🔑 Why Act Now")
        reasons = [
            ("🏛️", "Digital India 2.0",    "₹1.2T govt spend on SME digitization"),
            ("📱", "Mobile-First India",   "91% SMEs on mobile, 5G in 500+ cities"),
            ("🤖", "Open-Source LLMs",     "Llama 3 & Sarvam AI cut infra costs 70%"),
            ("💳", "UPI + ONDC",           "200M SMEs gaining digital commerce rails"),
            ("📊", "No Dominant Player",   "Market is fragmented, no clear winner yet"),
        ]
        for icon, title, desc in reasons:
            st.markdown(f"""
            <div class="info-block">
              <div class="ib-title">{icon} {title}</div>
              <div class="ib-note" style="color:#94A3B8;font-size:13px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🎯 Project Scope")
    c1, c2, c3, c4, c5 = st.columns(5)
    steps = [("01", "Market Research", "TAM/SAM/SOM + competitors"),
             ("02", "Industry Analysis", "Porter's Five Forces"),
             ("03", "Customer Insights", "42 SME surveys"),
             ("04", "Financial Model",   "Revenue + CAC"),
             ("05", "Strategy",          "GTM + pricing plan")]
    for col, (num, title, sub) in zip([c1,c2,c3,c4,c5], steps):
        with col:
            html = (
                '<div class="kpi-card" style="padding:14px;">'
                '<div style="font-size:11px;color:' + MINT + ';font-weight:700;letter-spacing:0.1em;">' + num + '</div>'
                '<div style="font-size:14px;font-weight:600;color:#fff;margin:6px 0 4px 0;">' + title + '</div>'
                '<div style="font-size:11px;color:' + MUTED + ';">' + sub + '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# SLIDE 2: MARKET SIZING
# ──────────────────────────────────────────────────────────────────
elif active == "🌏 Market Sizing":
    slide_header("Market Sizing: TAM / SAM / SOM", "Bottom-up analysis across 63M+ Indian SMEs")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top:4px solid {TEAL};">
          <div style="font-size:11px;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">TAM — Total Addressable Market</div>
          <div style="font-size:38px;font-weight:700;color:{SKY};margin:8px 0;">$18.5B</div>
          <div style="font-size:12px;color:{MUTED};">by 2028</div>
          <hr style="border-color:#1E3A4F;margin:12px 0;">
          <div style="font-size:12px;color:#94A3B8;">63M SMEs × avg $294/yr AI spend potential</div>
          <div style="font-size:12px;color:#94A3B8;margin-top:6px;">Covers all Indian businesses addressable by AI tools, including enterprises, mid-market & SMEs</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top:4px solid {TEAL};">
          <div style="font-size:11px;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">SAM — Serviceable Addressable Market</div>
          <div style="font-size:38px;font-weight:700;color:{MINT};margin:8px 0;">$4.5B</div>
          <div style="font-size:12px;color:{MUTED};">by 2028</div>
          <hr style="border-color:#1E3A4F;margin:12px 0;">
          <div style="font-size:12px;color:#94A3B8;">~15.3M SMEs × $294/yr (24% adoption potential)</div>
          <div style="font-size:12px;color:#94A3B8;margin-top:6px;">Tech-enabled SMEs in Tier 1 & 2 cities with internet access & willingness to pay for SaaS</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top:4px solid {MINT};">
          <div style="font-size:11px;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">SOM — Serviceable Obtainable Market</div>
          <div style="font-size:38px;font-weight:700;color:{GOLD};margin:8px 0;">$135M</div>
          <div style="font-size:12px;color:{MUTED};">Year 3 target</div>
          <hr style="border-color:#1E3A4F;margin:12px 0;">
          <div style="font-size:12px;color:#94A3B8;">45,000 paying SMEs × ₹25,000/yr avg ARR</div>
          <div style="font-size:12px;color:#94A3B8;margin-top:6px;">3% SAM penetration via aggressive GTM, referral loop & freemium → paid conversion</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown("#### 🥧 Market Share Breakdown by Segment")
        labels = ["Enterprise AI (Locked)", "Mid-Market AI", "SME Untapped (Our Target)", "Consumer AI"]
        values = [28, 19, 39, 14]
        colors = [TEAL, SKY, MINT, MUTED]
        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.52,
            marker=dict(colors=colors, line=dict(color=CARD, width=3)),
            textinfo="percent+label",
            textfont=dict(size=12, color="white"),
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=340,
            annotations=[dict(text="$18.5B<br>TAM", x=0.5, y=0.5, font=dict(size=15, color=MINT), showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### 📍 City-Tier Distribution")
        tiers = ["Tier 1 Cities<br>(8 cities)", "Tier 2 Cities<br>(50+ cities)", "Tier 3+ Cities<br>(500+ cities)"]
        smecounts = [3.2, 8.1, 51.7]
        pct_digital = [72, 44, 18]
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(
            x=tiers, y=smecounts, name="SMEs (Mn)",
            marker=dict(color=TEAL, opacity=0.8), text=[f"{v}M" for v in smecounts],
            textposition="outside", textfont=dict(color="#CBD5E1"),
        ), secondary_y=False)
        fig2.add_trace(go.Scatter(
            x=tiers, y=pct_digital, name="% Digitally Active",
            mode="lines+markers+text",
            line=dict(color=MINT, width=2),
            marker=dict(color=MINT, size=9),
            text=[f"{v}%" for v in pct_digital],
            textposition="top center",
            textfont=dict(color=MINT),
        ), secondary_y=True)
        fig2.update_layout(**PLOTLY_LAYOUT, height=330,
            legend=dict(orientation="h", y=-0.15, font=dict(size=11)),
            yaxis=dict(title="SME Count (Million)", gridcolor="#1E3A4F"),
            yaxis2=dict(title="% Digitally Active", gridcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#1E3A4F"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📐 Sizing Methodology")
    tab1, tab2, tab3 = st.tabs(["TAM Calculation", "SAM Calculation", "SOM Calculation"])
    with tab1:
        st.markdown("""
        | Input | Value | Source |
        |---|---|---|
        | Total registered Indian SMEs | 63.4 Million | MSME Ministry, 2024 |
        | Average AI-addressable spend/yr (if adopted) | $294 | IDC India, 2025 |
        | TAM = SMEs × Avg Spend | **$18.5B** | Bottom-up model |
        | Growth rate (CAGR 2024–28) | 38% | NASSCOM AI Report |
        """)
    with tab2:
        st.markdown("""
        | Input | Value | Source |
        |---|---|---|
        | SMEs with internet + smartphone access | 15.3 Million (24%) | TRAI, 2024 |
        | Demonstrated willingness to pay (survey) | 64% | Primary research (n=42) |
        | SAM = Addressable SMEs × Avg Spend | **$4.5B** | Bottom-up |
        | Key filters | Tier 1/2 cities, existing SaaS adoption | — |
        """)
    with tab3:
        st.markdown("""
        | Input | Value | Assumption |
        |---|---|---|
        | Paying SMEs in Year 3 | 45,000 | 3% SAM penetration |
        | Average ARR per SME | ₹25,000/yr (~$300) | ₹1,499/mo blended ARPU |
        | SOM Revenue Target | **₹112Cr ($135M)** | Conservative case |
        | Optimistic case (5% pen.) | ₹187Cr | Assumes strong viral loop |
        """)


# ──────────────────────────────────────────────────────────────────
# SLIDE 3: COMPETITIVE LANDSCAPE
# ──────────────────────────────────────────────────────────────────
elif active == "⚔️ Competitors":
    slide_header("Competitive Landscape", "30+ players analyzed across 4 market segments")

    # Bubble chart: price vs SME focus vs AI depth
    companies = [
        ("Microsoft Copilot",   3199, 15, 95, RED,   "Enterprise"),
        ("Salesforce Einstein", 4200, 10, 90, RED,   "Enterprise"),
        ("Google Workspace AI", 1899, 22, 80, RED,   "Enterprise"),
        ("Zoho AI Suite",        999, 72, 62, TEAL,  "Indian SME"),
        ("Freshworks Neo",      1899, 50, 65, TEAL,  "Indian SME"),
        ("Vyapar",               249, 92, 20, GREEN, "Indian SME"),
        ("OkCredit/Khatabook",   149, 90, 15, GREEN, "Indian SME"),
        ("Jasper.ai",           2999, 25, 78, SKY,   "Global SME"),
        ("HubSpot AI",          1600, 45, 72, SKY,   "Global SME"),
        ("Sarvam AI",           2500, 62, 80, GOLD,  "Indian GenAI"),
        ("Yellow.ai",           3000, 55, 75, GOLD,  "Indian GenAI"),
        ("Haptik",              2200, 60, 70, GOLD,  "Indian GenAI"),
        ("OUR TARGET",           999, 95, 75, MINT,  "Our Position"),
    ]

    df_comp = pd.DataFrame(companies, columns=["Company", "Price_INR", "SME_Focus", "AI_Depth", "Color", "Segment"])

    fig = go.Figure()
    for seg in df_comp["Segment"].unique():
        sub = df_comp[df_comp["Segment"] == seg]
        fig.add_trace(go.Scatter(
            x=sub["Price_INR"], y=sub["SME_Focus"],
            mode="markers+text",
            name=seg,
            text=sub["Company"],
            textposition="top center",
            textfont=dict(size=10, color="#CBD5E1"),
            marker=dict(
                size=sub["AI_Depth"] / 5,
                color=sub["Color"],
                opacity=0.85,
                line=dict(width=1, color="rgba(255,255,255,0.3)"),
            ),
        ))

    fig.update_layout(**PLOTLY_LAYOUT,
        height=420,
        title="Price (INR/mo) vs SME Focus % — bubble size = AI Depth score",
        xaxis=dict(title="Monthly Price (INR)", gridcolor="#1E3A4F"),
        yaxis=dict(title="SME Market Focus Score (%)", gridcolor="#1E3A4F"),
        legend=dict(orientation="h", y=-0.15, font=dict(size=11)),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📋 Detailed Benchmarking Table")
    benchmark = {
        "Company":          ["MS Copilot", "Zoho AI", "Freshworks", "Sarvam AI", "Jasper.ai", "Vyapar", "🎯 Our Target"],
        "Price/mo (INR)":   ["₹3,199",     "₹999",    "₹1,899",     "Custom",    "₹2,999",    "₹249",   "₹499–₹1,499"],
        "SME Focus":        ["Low",         "High",    "Medium",     "Medium",    "Low",        "V.High", "V.High"],
        "Languages":        ["English",     "Hindi+3", "English",    "22 lang",   "English",   "Hindi+5","22+ lang"],
        "AI Depth":         ["⭐⭐⭐⭐⭐", "⭐⭐⭐",   "⭐⭐⭐",     "⭐⭐⭐⭐",  "⭐⭐⭐⭐",  "⭐",      "⭐⭐⭐⭐"],
        "WhatsApp Native":  ["❌",          "❌",       "❌",          "Partial",   "❌",         "❌",      "✅"],
        "Offline Mode":     ["❌",          "❌",       "❌",          "Partial",   "❌",         "✅",      "✅"],
        "India Pricing":    ["❌",          "✅",       "Partial",    "✅",         "❌",         "✅",      "✅"],
    }
    df_bench = pd.DataFrame(benchmark)
    st.dataframe(
        df_bench.style.apply(lambda x: [
            f"background-color: #0a3020; color: {MINT}; font-weight: 700;" if "Our Target" in str(v) or "🎯" in str(v) else ""
            for v in x
        ], axis=1),
        use_container_width=True, hide_index=True
    )


# ──────────────────────────────────────────────────────────────────
# SLIDE 4: FIVE FORCES
# ──────────────────────────────────────────────────────────────────
elif active == "🔬 Five Forces":
    slide_header("Porter's Five Forces", "Overall Industry Attractiveness: HIGH ✅")

    forces_data = [
        ("Competitive Rivalry",        "MEDIUM", 3, GOLD,  "Fragmented: No single dominant SME-AI player in India. Fast-growing but not yet winner-take-all. 30+ players, none with >5% share."),
        ("Threat of New Entrants",     "HIGH",   4, RED,   "Low capital barriers + open-source LLMs (Llama 3, Mistral) enable fast new entry. VCs funding 8+ new GenAI startups monthly in India."),
        ("Buyer Power",                "LOW",    2, GREEN, "SMEs lack switching sophistication. High embedding once data & workflows are tied in. Price sensitive but very sticky once onboarded."),
        ("Supplier Power",             "MEDIUM", 3, GOLD,  "Dependency on OpenAI / Anthropic APIs (moderate risk). Mitigation: open-source LLMs + Sarvam infra + multi-LLM architecture. GPU costs falling 30%/yr."),
        ("Threat of Substitutes",      "LOW",    1, GREEN, "Traditional spreadsheets & manual ops are poor substitutes. No-code tools don't fully solve AI use cases for SMEs at this depth."),
    ]

    # Radar chart
    categories = [f[0] for f in forces_data]
    scores     = [f[2] for f in forces_data]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor=f"rgba(0,196,167,0.18)",
        line=dict(color=MINT, width=2),
        name="Threat Level",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor=CARD,
            radialaxis=dict(visible=True, range=[0, 5], gridcolor="#1E3A4F", color=MUTED, tickfont=dict(size=10)),
            angularaxis=dict(gridcolor="#1E3A4F", tickfont=dict(size=11, color="#CBD5E1")),
        ),
        paper_bgcolor=CARD,
        font=dict(color="#CBD5E1"),
        height=380,
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=40),
    )

    col_radar, col_detail = st.columns([2, 3])
    with col_radar:
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="kpi-card" style="margin-top:12px;">
          <div style="font-size:11px;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">Overall Verdict</div>
          <div style="font-size:26px;font-weight:700;color:{MINT};margin:8px 0;">ATTRACTIVE ✅</div>
          <div style="font-size:12px;color:#94A3B8;">Low buyer + substitute threat outweighs new entrant risk. Enter and build moat fast.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_detail:
        for name, rating, score, color, detail in forces_data:
            bar_pct = int(score / 5 * 100)
            st.markdown(f"""
            <div class="force-table-row">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <div style="font-weight:600;color:#fff;font-size:14px;">{name}</div>
                <div style="font-size:12px;font-weight:700;color:{color};background:rgba(0,0,0,0.2);
                     padding:2px 10px;border-radius:20px;border:1px solid {color};">{rating}</div>
              </div>
              <div style="background:#1E3A4F;border-radius:4px;height:4px;margin-bottom:8px;">
                <div style="background:{color};height:4px;border-radius:4px;width:{bar_pct}%;"></div>
              </div>
              <div style="font-size:12px;color:#94A3B8;">{detail}</div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# SLIDE 5: CUSTOMER INSIGHTS
# ──────────────────────────────────────────────────────────────────
elif active == "💬 Customer Insights":
    slide_header("Customer Insights", "Survey of 42 Indian SMEs across Retail, Manufacturing, Services, F&B")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("42",   "SMEs Surveyed",  "Tier 1 & 2 cities")
    with c2: kpi_card("78%",  "Prefer vernacular AI",  "Hindi, Tamil, Telugu, Kannada")
    with c3: kpi_card("64%",  "Willing to pay ₹499–₹1,499/mo",  "With clear ROI proof")
    with c4: kpi_card("91%",  "Mobile-first",  "Primary device for business tools")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        st.markdown("#### 📊 AI Awareness Levels")
        categories = ["Unaware", "Aware, never tried", "Trialed free tools", "Currently using", "Paid subscriber"]
        values = [10, 33, 26, 21, 10]
        colors = [MUTED, TEAL, SKY, MINT, GREEN]
        fig = go.Figure(go.Bar(
            x=values, y=categories,
            orientation="h",
            marker=dict(color=colors),
            text=[f"{v}%" for v in values],
            textposition="outside",
            textfont=dict(color="#CBD5E1"),
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=280,
            xaxis=dict(range=[0, 45], title="% of respondents", gridcolor="#1E3A4F"),
            yaxis=dict(autorange="reversed", gridcolor="#1E3A4F"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### 🏆 Top AI Use Cases by SME Demand")
        use_cases = ["WhatsApp Customer Bot", "GST / Invoice AI", "Vernacular Content Gen",
                     "Inventory Forecasting", "HR & Hiring AI", "Credit Scoring AI"]
        demand = [84, 79, 71, 67, 54, 48]
        effort_score = [20, 45, 25, 75, 55, 85]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=demand, y=use_cases, orientation="h",
            marker=dict(color=[MINT]*3 + [TEAL]*2 + [GOLD]*1, opacity=0.85),
            text=[f"{v}%" for v in demand],
            textposition="outside",
            textfont=dict(color="#CBD5E1"),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=280,
            xaxis=dict(range=[0, 100], title="% SMEs want this feature", gridcolor="#1E3A4F"),
            yaxis=dict(autorange="reversed", gridcolor="#1E3A4F"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💡 Key Qualitative Findings")
    findings = [
        ("78%", "prefer AI tools in their native language (Hindi, Tamil, Telugu, Kannada)",          "Language Gap Opportunity"),
        ("64%", "willing to pay ₹499–₹1,499/mo — if ROI is clearly demonstrated upfront",           "Pricing Validation"),
        ("91%", "use business tools primarily on mobile — desktop/laptop is secondary or unused",    "Mobile-First Design"),
        ("55%", "would switch current tool if WhatsApp-native integration was offered",              "Distribution Insight"),
        ("67%", "\"don't know how to tell if AI is helping our business\" — biggest stated barrier", "Onboarding Opportunity"),
    ]
    for stat, finding, label in findings:
        c1, c2 = st.columns([1, 5])
        with c1:
            st.markdown(f'<div style="font-size:26px;font-weight:700;color:{MINT};text-align:center;margin-top:8px;">{stat}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="info-block">
              <div style="display:flex;gap:8px;align-items:center;">
                <div class="ib-title" style="margin:0;">{finding}</div>
                <span class="chip">{label}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# SLIDE 6: FINANCIAL MODEL
# ──────────────────────────────────────────────────────────────────
elif active == "💹 Financial Model":
    slide_header("Financial Model", "Revenue Projections, Unit Economics & Break-Even Analysis")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("₹27Cr",    "ARR — Year 1",    "1,800 paying SMEs")
    with c2: kpi_card("₹89Cr",    "ARR — Year 2",    "5,940 paying SMEs")
    with c3: kpi_card("₹253Cr",   "ARR — Year 3",    "16,875 paying SMEs")
    with c4: kpi_card("Month 18", "Break-Even",       "62% gross margin")

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Revenue Model", "Unit Economics", "Scenario Analysis"])

    with tab1:
        quarters = ["Q1 Y1","Q2 Y1","Q3 Y1","Q4 Y1","Q1 Y2","Q2 Y2","Q3 Y2","Q4 Y2","Q1 Y3","Q2 Y3","Q3 Y3","Q4 Y3"]
        arr      = [2, 5, 11, 20, 29, 38, 55, 72, 90, 120, 155, 193]
        smes_q   = [150, 350, 750, 1250, 1900, 2700, 3800, 5000, 6800, 9200, 12500, 16000]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=quarters, y=arr, name="ARR (₹Cr)",
            marker=dict(color=TEAL, opacity=0.85),
            text=[f"₹{v}Cr" for v in arr],
            textposition="outside", textfont=dict(size=9, color="#CBD5E1"),
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=quarters, y=smes_q, name="Paying SMEs",
            mode="lines+markers",
            line=dict(color=MINT, width=2),
            marker=dict(color=MINT, size=7),
        ), secondary_y=True)
        # Breakeven annotation
        fig.add_vline(x="Q2 Y2", line_dash="dash", line_color=GOLD, line_width=1.5)
        fig.add_annotation(x="Q2 Y2", y=max(arr)*0.7, text="Break-Even ↑", font=dict(color=GOLD, size=11), showarrow=False)
        fig.update_layout(**PLOTLY_LAYOUT, height=380,
            legend=dict(orientation="h", y=-0.15),
            yaxis=dict(title="ARR (₹ Crore)", gridcolor="#1E3A4F"),
            yaxis2=dict(title="Paying SMEs", gridcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#1E3A4F"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Assumptions
        st.markdown("#### 📐 Model Assumptions")
        assump = pd.DataFrame({
            "Metric":             ["Paying SMEs", "Avg ARPU/mo", "Monthly Churn", "Gross Margin", "Net Rev Retention"],
            "Year 1":             ["1,800", "₹1,249", "4.5%", "62%", "95%"],
            "Year 2":             ["5,940", "₹1,399", "3.2%", "70%", "108%"],
            "Year 3":             ["16,875", "₹1,499", "2.5%", "76%", "115%"],
        })
        st.dataframe(assump, use_container_width=True, hide_index=True)

    with tab2:
        funnel_stages = ["Awareness (500K)", "Free Trial (25K)", "Activated (8.75K)", "Paid (1.75K)"]
        funnel_vals   = [500000, 25000, 8750, 1750]
        funnel_colors = [MUTED, TEAL, SKY, MINT]
        fig2 = go.Figure(go.Funnel(
            y=funnel_stages, x=funnel_vals,
            marker=dict(color=funnel_colors),
            textinfo="value+percent initial",
            textfont=dict(color="white", size=13),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=280, title="SME Acquisition Funnel (Year 1)",
            xaxis=dict(gridcolor="#1E3A4F"), yaxis=dict(gridcolor="#1E3A4F"))
        st.plotly_chart(fig2, use_container_width=True)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            info_block("Blended CAC", "₹3,750", "Per paid SME — Year 1 blended")
            info_block("LTV (24 months)", "₹28,760", "At 2.5% monthly churn, ₹1,499 ARPU")
        with col_b:
            info_block("LTV : CAC Ratio", "7.7x", "Target >3x — Healthy ✅")
            info_block("Payback Period", "3.5 months", "Blended average Year 1")
        with col_c:
            info_block("Gross Margin", "62–76%", "Improving with scale (infra efficiency)")
            info_block("NRR (Year 3)", "115%", "Expansion revenue > churn")

    with tab3:
        st.markdown("#### 📊 3-Scenario Revenue Projection (₹ Crore ARR, Year 3)")
        scenarios = {
            "Conservative (2% SAM)": [12, 27, 45, 68, 89, 112, 140, 165, 193],
            "Base Case (3% SAM)":    [18, 40, 65, 92, 125, 158, 195, 235, 280],
            "Optimistic (5% SAM)":   [25, 60, 100, 145, 190, 240, 295, 360, 430],
        }
        qs = ["Q1", "Q2", "Q3", "Q4 Y1", "Q1", "Q2", "Q3", "Q4 Y2", "Q1+"]
        fig3 = go.Figure()
        colors3 = [TEAL, MINT, GOLD]
        dashes3 = ["dash", "solid", "dot"]
        for (name, vals), col, dash in zip(scenarios.items(), colors3, dashes3):
            fig3.add_trace(go.Scatter(
                x=qs, y=vals, name=name,
                mode="lines+markers",
                line=dict(color=col, width=2.5, dash=dash),
                marker=dict(color=col, size=7),
                fill="tonexty" if name != "Conservative (2% SAM)" else None,
                fillcolor=f"rgba(26,107,138,0.12)",
            ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=350,
            legend=dict(orientation="h", y=-0.15),
            xaxis=dict(gridcolor="#1E3A4F"), yaxis=dict(gridcolor="#1E3A4F"))
        st.plotly_chart(fig3, use_container_width=True)


# ──────────────────────────────────────────────────────────────────
# SLIDE 7: GO-TO-MARKET
# ──────────────────────────────────────────────────────────────────
elif active == "🚀 Go-to-Market":
    slide_header("Go-to-Market Strategy", "Enter Now · Localize Deeply · Win Indian SME AI")

    st.markdown("#### 🗺️ 3-Phase Entry Roadmap")
    col1, col2, col3 = st.columns(3)

    phases = [
        ("Phase 1", "Months 1–6", "Beachhead Entry", TEAL, [
            "Launch in Mumbai, Bengaluru, Jaipur",
            "Focus: Retail & Services SMEs only",
            "WhatsApp-first onboarding (zero friction)",
            "Freemium tier to build trust & data",
        ]),
        ("Phase 2", "Months 7–18", "Expand & Deepen", NAV, [
            "Expand to 15 Tier 1 + Tier 2 cities",
            "Add Manufacturing & F&B verticals",
            "Launch Hindi + Tamil + Telugu UX",
            "Build referral flywheel (₹500 credit)",
        ]),
        ("Phase 3", "Months 19–36", "Scale & Platform", MINT, [
            "Pan-India (100+ cities)",
            "Marketplace of 3rd-party AI agents",
            "Embedded lending + insurance upsell",
            "API-first B2B2C via banks & telcos",
        ]),
    ]

    for col, (phase, period, title, color, points) in zip([col1,col2,col3], phases):
        bullet_html = "".join(['<li style="margin:8px 0;font-size:13px;color:#CBD5E1;">' + p + '</li>' for p in points])
        with col:
            html = (
                '<div style="background:' + color + ';border-radius:10px 10px 0 0;padding:14px 18px;">'
                '<div style="font-size:11px;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.1em;">' + phase + ' · ' + period + '</div>'
                '<div style="font-size:18px;font-weight:700;color:#fff;margin-top:4px;">' + title + '</div>'
                '</div>'
                '<div style="background:' + CARD + ';border:1px solid #1E3A4F;border-top:none;border-radius:0 0 10px 10px;padding:18px;">'
                '<ul style="padding-left:18px;margin:0;">' + bullet_html + '</ul>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💰 Pricing Tiers")
    p1, p2, p3 = st.columns(3)

    tiers = [
        ("Free",    "₹0",     "/forever", MUTED, ["1 AI assistant", "WhatsApp bot", "500 messages/mo", "Hindi only"], "Freemium Hook"),
        ("Starter", "₹499",   "/month",   TEAL,  ["3 AI assistants", "GST filing AI", "5,000 msg/mo",  "5 languages"], "⭐ Most Popular"),
        ("Growth",  "₹1,499", "/month",   MINT,  ["Unlimited agents", "Inventory AI",  "Unlimited usage", "22 langs + API"], "Power Users"),
    ]
    for col, (name, price, period, color, feats, tag) in zip([p1, p2, p3], tiers):
        feat_html = "".join(['<div style="padding:5px 0;border-bottom:1px solid #1E3A4F;font-size:13px;color:#CBD5E1;">✓ ' + f + '</div>' for f in feats])
        with col:
            html = (
                '<div class="kpi-card" style="text-align:left;border-top:4px solid ' + color + ';">'
                '<div style="font-size:11px;color:' + MUTED + ';text-transform:uppercase;letter-spacing:0.1em;">' + name + '</div>'
                '<div style="font-size:34px;font-weight:700;color:' + color + ';margin:8px 0 2px 0;">' + price + '</div>'
                '<div style="font-size:12px;color:' + MUTED + ';margin-bottom:14px;">' + period + '</div>'
                + feat_html +
                '<div style="margin-top:14px;background:' + color + ';opacity:0.15;border-radius:6px;padding:6px 12px;text-align:center;">'
                '<span style="font-size:12px;font-weight:700;color:' + color + ';opacity:1;">' + tag + '</span>'
                '</div></div>'
            )
            st.markdown(html, unsafe_allow_html=True)

    st.markdown("<br>")
    st.markdown("#### 📡 GTM Distribution Channels")
    channels = [
        ("📲", "WhatsApp Native",    "530M users, zero-install onboarding, highest SME trust channel in India"),
        ("🏦", "NBFC / Bank Embed",  "Partner with Bajaj Finserv, HDFC SME banking — embedded AI upsell at account opening"),
        ("🛒", "ONDC / Dukaan",      "Hook into commerce platforms where SMEs already transact — AI as native feature"),
        ("🤝", "CA / Tax Partners",  "75,000 CAs serve Indian SMEs — trusted referral network, 30% referral fee"),
        ("🎓", "Govt / Startup Hubs","NASSCOM CoE, MSME DI, Startup India — credibility + subsidized distribution"),
        ("📢", "WhatsApp Ads",       "Meta Business Manager — hyper-targeted SME ads in Hindi at ₹8–12 CPM"),
    ]
    c1, c2 = st.columns(2)
    for i, (icon, name, desc) in enumerate(channels):
        with (c1 if i % 2 == 0 else c2):
            st.markdown(f"""
            <div class="info-block">
              <div class="ib-title">{icon} {name}</div>
              <div style="font-size:12px;color:#94A3B8;margin-top:4px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# SLIDE 8: LIVE DASHBOARD
# ──────────────────────────────────────────────────────────────────
elif active == "📡 Live Dashboard":
    # Header with live badge
    col_h, col_badge = st.columns([4, 1])
    with col_h:
        slide_header("Live Operations Dashboard", "Real-time KPI monitoring · Auto-refreshes on toggle")
    with col_badge:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.auto_refresh:
            st.markdown('<div class="live-badge" style="margin-top:14px;"><div class="live-dot"></div>LIVE SYNC ON</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:12px;color:#64748B;margin-top:20px;">Toggle Live Sync in sidebar →</div>', unsafe_allow_html=True)

    # Real-time KPIs
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Active SMEs", f"{st.session_state.live_smes:,}",
                  delta=f"+{random.randint(1,8)} today", delta_color="normal")
    with k2:
        st.metric("MRR (₹)", f"₹{st.session_state.live_mrr:,.0f}",
                  delta=f"+₹{random.randint(5000,20000):,}", delta_color="normal")
    with k3:
        st.metric("Churn Rate", f"{st.session_state.live_churn:.2f}%",
                  delta=f"{random.choice(['-0.02%', '-0.01%', '+0.01%'])}", delta_color="inverse")
    with k4:
        st.metric("NPS Score", f"{st.session_state.live_nps}",
                  delta=f"{random.choice(['+1', '+2', '0'])}", delta_color="normal")
    with k5:
        st.metric("CAC (₹)", f"₹{st.session_state.live_cac:,}",
                  delta=f"₹{random.randint(-50,30)}", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Live sparkline charts
    left_c, right_c = st.columns(2)

    with left_c:
        st.markdown("#### 📈 MRR — Live Trend (Last 30 ticks)")
        fig_mrr = go.Figure()
        fig_mrr.add_trace(go.Scatter(
            x=st.session_state.history_ts,
            y=st.session_state.history_mrr,
            mode="lines",
            line=dict(color=MINT, width=2.5),
            fill="tozeroy",
            fillcolor=f"rgba(0,196,167,0.10)",
        ))
        fig_mrr.add_trace(go.Scatter(
            x=[st.session_state.history_ts[-1]],
            y=[st.session_state.history_mrr[-1]],
            mode="markers+text",
            marker=dict(color=MINT, size=10),
            text=[f"₹{st.session_state.history_mrr[-1]:,.0f}"],
            textposition="top right",
            textfont=dict(color=MINT, size=11),
            showlegend=False,
        ))
        fig_mrr.update_layout(**PLOTLY_LAYOUT, height=240,
            xaxis=dict(showticklabels=False, gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(title="MRR (₹)", gridcolor="#1E3A4F"),
        )
        st.plotly_chart(fig_mrr, use_container_width=True)

    with right_c:
        st.markdown("#### 👥 Active SMEs — Live Count")
        fig_sme = go.Figure()
        fig_sme.add_trace(go.Scatter(
            x=st.session_state.history_ts,
            y=st.session_state.history_smes,
            mode="lines",
            line=dict(color=SKY, width=2.5),
            fill="tozeroy",
            fillcolor=f"rgba(79,195,247,0.10)",
        ))
        fig_sme.add_trace(go.Scatter(
            x=[st.session_state.history_ts[-1]],
            y=[st.session_state.history_smes[-1]],
            mode="markers+text",
            marker=dict(color=SKY, size=10),
            text=[f"{st.session_state.history_smes[-1]:,}"],
            textposition="top right",
            textfont=dict(color=SKY, size=11),
            showlegend=False,
        ))
        fig_sme.update_layout(**PLOTLY_LAYOUT, height=240,
            xaxis=dict(showticklabels=False, gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(title="Active Paying SMEs", gridcolor="#1E3A4F"),
        )
        st.plotly_chart(fig_sme, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🌐 Live SME Signups by City (Simulated)")
    cities = ["Mumbai", "Bengaluru", "Delhi NCR", "Hyderabad", "Pune", "Chennai",
              "Jaipur", "Ahmedabad", "Kolkata", "Lucknow", "Surat", "Indore"]
    signups = [random.randint(80, 350) for _ in cities]
    revenue = [s * random.randint(900, 1600) for s in signups]

    fig_city = go.Figure()
    fig_city.add_trace(go.Bar(
        x=cities, y=signups,
        marker=dict(
            color=signups,
            colorscale=[[0, TEAL], [0.5, MINT], [1.0, SKY]],
            showscale=False,
        ),
        text=[f"{v}" for v in signups],
        textposition="outside",
        textfont=dict(color="#CBD5E1", size=10),
    ))
    fig_city.update_layout(**PLOTLY_LAYOUT, height=280,
        xaxis=dict(title="City", gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(title="New Signups (This Month)", gridcolor="#1E3A4F"),
    )
    st.plotly_chart(fig_city, use_container_width=True)

    st.markdown("#### 📋 Latest Activity Feed")
    events = [
        ("🟢", datetime.now().strftime("%H:%M:%S"), "New signup", "Sharma Traders, Jaipur — Starter Plan"),
        ("💳", (datetime.now() - timedelta(seconds=12)).strftime("%H:%M:%S"), "Payment", "₹1,499 MRR locked — Khanna Textiles, Surat"),
        ("⬆️", (datetime.now() - timedelta(seconds=28)).strftime("%H:%M:%S"), "Upgrade", "Free → Starter — Meena Boutique, Bengaluru"),
        ("🤝", (datetime.now() - timedelta(seconds=45)).strftime("%H:%M:%S"), "Referral", "Patel Motors referred 3 new signups — ₹1,500 credit issued"),
        ("❌", (datetime.now() - timedelta(seconds=90)).strftime("%H:%M:%S"), "Churn", "Gupta Electronics cancelled — reason: price sensitivity"),
        ("🟢", (datetime.now() - timedelta(seconds=130)).strftime("%H:%M:%S"), "New signup", "Arora Pharma Dist, Lucknow — Growth Plan"),
    ]
    for icon, ts, event_type, detail in events:
        html = (
            '<div style="display:flex;gap:14px;align-items:flex-start;'
            'padding:8px 0;border-bottom:1px solid #1E3A4F;">'
            '<div style="font-size:16px;">' + icon + '</div>'
            '<div style="font-size:11px;color:' + MUTED + ';white-space:nowrap;margin-top:2px;">' + ts + '</div>'
            '<div>'
            '<span style="font-size:12px;font-weight:600;color:' + MINT + ';">' + event_type + '</span>'
            '<span style="font-size:12px;color:#94A3B8;margin-left:8px;">' + detail + '</span>'
            '</div></div>'
        )
        st.markdown(html, unsafe_allow_html=True)
