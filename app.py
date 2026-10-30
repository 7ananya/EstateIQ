
import re
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="EstateIQ | Mumbai Property Intelligence", page_icon="🏙️", layout="wide", initial_sidebar_state="collapsed")
DATA_PATH = Path(__file__).parent / "data" / "Mumbai_property_details.csv"
if not DATA_PATH.exists():
    DATA_PATH = Path(__file__).parent / "Mumbai_property_details.csv"

# ---------- Design system ----------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#242923; --muted:#6e746b; --cream:#f4efe5; --paper:#fffdf8; --teal:#477568; --orange:#c8754d; --line:#e4dbcc; --sand:#e8ddca; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:var(--cream); color:var(--ink); }
.stApp { color:var(--ink); }
/* Keep custom component colours intact; avoid broad descendant selectors overriding component styles. */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color:var(--ink); }
.section-title { color:var(--ink) !important; }
.metric-value { color:var(--ink) !important; }
.metric-label { color:#59665f !important; }
.metric-note, .section-sub, .showcase-copy { color:var(--muted) !important; }
.showcase-kicker, .showcase-heading, .showcase-copy { opacity:1; }
.showcase-kicker { color:var(--teal) !important; }
.showcase-heading { color:var(--ink) !important; }
.feature-icon { color:var(--teal) !important; }
.footer { color:#656b62 !important; }
.stApp [data-testid="stMarkdownContainer"] h1, .stApp [data-testid="stMarkdownContainer"] h2, .stApp [data-testid="stMarkdownContainer"] h3 { color:var(--ink) !important; }
.stApp [data-testid="stMarkdownContainer"] p, .stApp [data-testid="stCaptionContainer"] p { color:var(--muted); }
/* Keep the hero text white over the photograph; override Streamlit's global text rules. */
.stApp .hero h1, .stApp [data-testid="stMarkdownContainer"] .hero h1 { color:#ffffff !important; }
.stApp .hero p, .stApp [data-testid="stMarkdownContainer"] .hero p { color:#ffffff !important; }
.stApp [data-baseweb="select"] *, .stApp input, .stApp textarea { color:var(--ink) !important; }
.stApp [data-testid="stMultiSelect"] label, .stApp [data-testid="stSlider"] label { color:var(--ink) !important; }
.block-container { max-width:1440px; padding-top:1rem; padding-bottom:3rem; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility:hidden; }
section[data-testid="stSidebar"] { background:#122e37; }
.brand {font-family:'Manrope',sans-serif;font-size:1.65rem;font-weight:800;letter-spacing:-1px;color:#142d32;}
.brand span {color:var(--orange)}
.eyebrow {font-size:.73rem;letter-spacing:2px;font-weight:700;text-transform:uppercase;color:var(--teal);}
.hero {background:linear-gradient(90deg,rgba(30,39,33,.72),rgba(30,39,33,.12)),url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=2000&q=85');background-size:cover;background-position:center;border-radius:22px;padding:58px 54px;color:white;min-height:360px;display:flex;flex-direction:column;justify-content:center;margin:12px 0 22px;}
.hero h1 {font-family:'Manrope',sans-serif;font-size:clamp(2.2rem,4.6vw,4.2rem);font-weight:800;line-height:1.04;letter-spacing:-2px;max-width:760px;margin:.6rem 0 1rem;color:#fff;}
.hero p {font-size:1.04rem;line-height:1.65;max-width:640px;color:#f1f4ef;}
.pill {display:inline-block;background:#e4f4ed;color:#12665d;border-radius:30px;padding:7px 12px;font-size:.76rem;font-weight:700;letter-spacing:.3px;width:max-content;}
.section-title {font-family:'Manrope',sans-serif;font-weight:800;letter-spacing:-.8px;font-size:1.8rem;margin:.15rem 0 .35rem;}
.section-sub {color:var(--muted);margin-bottom:1.2rem;}
.feature-card {background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:22px 23px;height:100%;}
.feature-icon {font-size:1.55rem;background:#e9e3d5;border-radius:13px;padding:10px;display:inline-block;margin-bottom:14px;}
.feature-card h3 {font-family:'Manrope',sans-serif;font-size:1.1rem;margin:.2rem 0 .5rem;color:var(--ink);}
.feature-card p {font-size:.91rem;color:var(--muted);line-height:1.55;}
.metric-card {background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:20px 22px;min-height:130px;}
.metric-label {font-size:.72rem;letter-spacing:1.2px;font-weight:700;color:#718079;text-transform:uppercase;}
.metric-value {font-family:'Manrope',sans-serif;font-size:1.8rem;font-weight:800;letter-spacing:-.8px;margin-top:9px;}
.metric-note {font-size:.8rem;color:var(--muted);margin-top:4px;}
.listing-card {background:white;border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin-bottom:10px;}
.footer {border-top:1px solid var(--line);padding-top:20px;margin-top:44px;color:#7c8580;font-size:.82rem;}
div.stButton > button {border-radius:999px;border:1px solid #d8cdbb;background:#fffdf8;color:#242923;font-weight:700;padding:.58rem 1rem;}
div.stButton > button:hover {border-color:#477568;color:#477568;}
.stButton button[kind="primary"] {background:var(--orange);border-color:var(--orange);color:white;}
[data-testid="stDataFrame"] {border:1px solid var(--line);border-radius:12px;overflow:hidden;}
[data-testid="stMetric"] {background:var(--paper);border:1px solid var(--line);border-radius:15px;padding:15px 18px;}
[data-testid="stMetricLabel"] {color:var(--muted) !important;}
[data-testid="stMetricValue"] {color:var(--ink) !important;}


/* Warm 3D property showcase */
.showcase-wrap { margin: 12px 0 30px; padding: 34px 26px 28px; border:1px solid #e5dac9; border-radius:24px; background:linear-gradient(135deg,#fffdf8 0%,#eee4d4 100%); overflow:hidden; }
.showcase-kicker {font-size:.72rem;letter-spacing:2px;text-transform:uppercase;font-weight:800;color:#477568;text-align:center;}
.showcase-heading {font-family:'Manrope',sans-serif;font-size:1.65rem;font-weight:800;letter-spacing:-.8px;text-align:center;color:#242923;margin:7px 0 4px;}
.showcase-copy {text-align:center;color:#6e746b;font-size:.93rem;margin-bottom:10px;}
.perspective-stage {height:310px;position:relative;display:flex;align-items:center;justify-content:center;perspective:1400px;margin:4px auto 0;max-width:1040px;}
.mock-panel {position:absolute;width:34%;height:245px;border:1px solid #e2d7c8;border-radius:13px;background:#fffdf8;box-shadow:0 22px 42px rgba(68,53,35,.18);overflow:hidden;transition:transform .35s ease,box-shadow .35s ease;}
.mock-panel:hover {box-shadow:0 30px 52px rgba(68,53,35,.24);z-index:8;}
.mock-panel.left {left:7%;transform:rotateY(24deg) rotateZ(-3deg) translateZ(-35px);}
.mock-panel.center {left:33%;width:36%;height:270px;z-index:3;transform:translateZ(55px) rotateY(-2deg);}
.mock-panel.right {right:7%;transform:rotateY(-24deg) rotateZ(3deg) translateZ(-35px);}
.mock-topbar {height:25px;border-bottom:1px solid #eee5d8;display:flex;align-items:center;gap:4px;padding:0 10px;background:#fff;}
.mock-dot {width:5px;height:5px;border-radius:50%;background:#d8c6ad;}
.mock-brand {font-size:8px;font-weight:800;letter-spacing:1.3px;color:#3e5f53;margin-left:5px;}
.mock-body {padding:13px 14px;color:#292d28;}
.mock-eyebrow {font-size:6px;letter-spacing:1.4px;color:#9a795a;font-weight:800;text-transform:uppercase;}
.mock-title {font-family:'Manrope',sans-serif;font-weight:800;font-size:15px;line-height:1.12;margin:6px 0 9px;color:#252923;}
.mock-panel.center .mock-title {font-size:19px;}
.mock-sub {font-size:7px;line-height:1.5;color:#77786f;max-width:190px;}
.mock-hero-photo {height:76px;border-radius:7px;background-size:cover;background-position:center;margin:9px 0;background-image:linear-gradient(0deg,rgba(33,44,35,.18),rgba(33,44,35,.02)),url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=700&q=80');}
.mock-panel.center .mock-hero-photo {height:94px;}
.mock-stats {display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-top:8px;}
.mock-stat {background:#f4efe5;border-radius:5px;padding:7px 5px;}
.mock-stat b {display:block;font-size:9px;color:#477568;}
.mock-stat span {font-size:6px;color:#77786f;}
.mock-line {height:5px;border-radius:4px;background:#eae2d6;margin:6px 0;width:82%;}
.mock-line.short {width:52%;}
