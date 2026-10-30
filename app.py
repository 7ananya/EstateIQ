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
.mock-chip {display:inline-block;border-radius:20px;background:#e6eee7;color:#477568;font-size:6px;padding:4px 7px;font-weight:800;margin-top:7px;}
.mock-listing {display:flex;gap:7px;align-items:center;border:1px solid #eee5d8;border-radius:6px;padding:6px;margin-top:7px;}
.mock-thumb {width:43px;height:34px;border-radius:4px;background-size:cover;background-position:center;background-image:url('https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=200&q=75');}
.mock-listing b {display:block;font-size:7px;color:#33382f;}
.mock-listing span {display:block;font-size:6px;color:#77786f;margin-top:3px;}
@media(max-width:760px){.showcase-wrap{padding:25px 12px}.perspective-stage{height:260px}.mock-panel{width:39%;height:205px}.mock-panel.left{left:0}.mock-panel.center{left:28%;width:44%;height:225px}.mock-panel.right{right:0}.mock-title{font-size:11px}.mock-panel.center .mock-title{font-size:14px}.mock-hero-photo{height:52px}.mock-panel.center .mock-hero-photo{height:65px}}

hr {border-color:var(--line);}
</style>
""", unsafe_allow_html=True)

# ---------- Data prep ----------
def parse_money(v):
    if pd.isna(v): return np.nan
    s=str(v).lower().strip().replace(',','').replace('₹','')
    m=re.fullmatch(r'([0-9]*\.?[0-9]+)\s*(lac|lakh|lacs|lakhs)',s)
    if m: return float(m.group(1))*100000
    m=re.fullmatch(r'([0-9]*\.?[0-9]+)\s*(cr|crore|crores)',s)
    if m: return float(m.group(1))*10000000
    try: return float(s)
    except: return np.nan

@st.cache_data
def load_data():
    raw=pd.read_csv(DATA_PATH)
    d=raw.copy()
    d['Monthly Rent (₹)']=d['Price'].map(parse_money)
    # Area cells sometimes contain a second unrelated number; use the first number as sq ft.
    d['Area (sq ft)']=pd.to_numeric(d['Area'].astype(str).str.extract(r'^\s*([\d,]+(?:\.\d+)?)')[0].str.replace(',','',regex=False),errors='coerce')
    d['BHK number']=pd.to_numeric(d['BHK'],errors='coerce')
    d['Locality']=d['Location'].astype(str).str.strip()
    if 'Description' in d.columns:
        extracted=d['Description'].astype(str).str.extract(r'for Rent in\s+(.*?)(?:,\s*Mumbai\b|$)',flags=re.I)[0]
        d['Locality']=extracted.fillna(d['Locality']).astype(str).str.strip()
    d['Locality']=d['Locality'].replace({'nan':'Unknown / missing','':'Unknown / missing'})
    d['Include baseline']=d['Monthly Rent (₹)'].notna() & d['Area (sq ft)'].notna() & (d['Monthly Rent (₹)']>0) & (d['Area (sq ft)']>0) & (d['Monthly Rent (₹)']<=1000000) & (~d['Price'].astype(str).str.contains(r'\bcr\b|crore',case=False,regex=True,na=False))
    return d

df_all=load_data(); data=df_all[df_all['Include baseline']].copy()
if data.empty:
    st.error('No usable records found. Check that the data CSV is present in the data folder.'); st.stop()

# ---------- State and navigation ----------
if 'page' not in st.session_state: st.session_state.page='Home'
def go(page): st.session_state.page=page

# Header / nav
head=st.columns([2.3,1,1,1,1.25])
with head[0]: st.markdown('<div class="brand">Estate<span>IQ</span> <span style="font-size:.72rem;color:#697570;font-weight:600;letter-spacing:1px;margin-left:7px">MUMBAI</span></div>',unsafe_allow_html=True)
for col,label in zip(head[1:],['Home','Explore listings','Investment lab','Market insights']):
    with col:
        if st.button(label, key='nav_'+label, use_container_width=True, type='primary' if st.session_state.page==label else 'secondary'): go(label)
st.markdown('<hr style="margin:12px 0 18px">',unsafe_allow_html=True)

# Sidebar assumptions apply across investment pages
with st.sidebar:
    st.markdown('<div style="font-size:1.5rem;font-weight:800;color:white">EstateIQ</div><div style="color:#b7cfce;letter-spacing:1.5px;font-size:.72rem">INVESTMENT MODEL</div>',unsafe_allow_html=True)
    st.divider()
    st.markdown('### Scenario assumptions')
    price_sqft=st.number_input('Assumed purchase price / sq ft (₹)',min_value=1000,max_value=200000,value=25000,step=1000)
    acquisition=st.number_input('Acquisition costs (%)',min_value=0.0,max_value=25.0,value=7.0,step=.5)
    vacancy=st.slider('Expected vacancy (%)',0,40,5)
    operating=st.slider('Operating costs (% of collected rent)',0,40,12)
    appreciation=st.number_input('Annual appreciation assumption (%)',min_value=-20.0,max_value=30.0,value=5.0,step=.5)
    years=st.slider('Holding period (years)',1,30,5)
    st.caption('Scenario assumptions only. Dataset prices are treated as rents, not verified purchase prices.')

# Compute common metrics
def calculate(frame):
    x=frame.copy()
    x['Estimated Purchase Price (₹)']=x['Area (sq ft)']*price_sqft
    x['Acquisition Cost (₹)']=x['Estimated Purchase Price (₹)']*(1+acquisition/100)
    x['Effective Annual Rent (₹)']=x['Monthly Rent (₹)']*12*(1-vacancy/100)
    x['Net Annual Rent (₹)']=x['Effective Annual Rent (₹)']*(1-operating/100)
    x['Gross Yield (%)']=x['Monthly Rent (₹)']*12/x['Estimated Purchase Price (₹)']*100
    x['Net Yield (%)']=x['Net Annual Rent (₹)']/x['Acquisition Cost (₹)']*100
    x['Payback Period (years)']=np.where(x['Net Annual Rent (₹)']>0,x['Acquisition Cost (₹)']/x['Net Annual Rent (₹)'],np.nan)
    x['Estimated Exit Value (₹)']=x['Estimated Purchase Price (₹)']*(1+appreciation/100)**years
    x['Estimated Total Gain (₹)']=x['Estimated Exit Value (₹)']-x['Acquisition Cost (₹)']+x['Net Annual Rent (₹)']*years
    x['Estimated Total Return (%)']=x['Estimated Total Gain (₹)']/x['Acquisition Cost (₹)']*100
    return x

def style_chart(fig):
    """Apply the site's warm ivory palette to every Plotly chart."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#fffdf8",
        plot_bgcolor="#fffdf8",
        font=dict(family="DM Sans, sans-serif", color="#343a33", size=12),
        title=dict(font=dict(family="Manrope, sans-serif", size=17, color="#242923"), x=0.02, xanchor="left"),
        margin=dict(l=24, r=20, t=64, b=36),
        legend=dict(bgcolor="rgba(255,253,248,0.85)", font=dict(color="#4f574f")),
        colorway=["#477568", "#c8754d", "#8e9f79", "#d6b887", "#6d8790", "#aa8b79", "#7d9278"]
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e9e2d6", zerolinecolor="#d9cfbf", linecolor="#ded5c8", tickfont=dict(color="#555d54"), title_font=dict(color="#424940"))
    fig.update_yaxes(showgrid=True, gridcolor="#e9e2d6", zerolinecolor="#d9cfbf", linecolor="#ded5c8", tickfont=dict(color="#555d54"), title_font=dict(color="#424940"))
    return fig

# ---------- Pages ----------
page=st.session_state.page
if page=='Home':
    st.markdown('<div class="hero"><div class="pill">MUMBAI PROPERTY INTELLIGENCE</div><h1>Find the right property.<br>Understand the numbers.</h1><p>Explore rental listings, compare neighbourhoods, and test real-estate investment scenarios with a transparent data-driven toolkit.</p></div>',unsafe_allow_html=True)
    st.markdown(r"""
    <div class="showcase-wrap">
      <div class="showcase-kicker">A closer look at EstateIQ</div>
      <div class="showcase-heading">Property discovery, with a clearer perspective.</div>
      <div class="showcase-copy">Browse listings, compare neighbourhoods, and see the numbers behind the opportunity.</div>
      <div class="perspective-stage">
        <div class="mock-panel left">
          <div class="mock-topbar"><i class="mock-dot"></i><i class="mock-dot"></i><i class="mock-dot"></i><span class="mock-brand">ESTATEIQ</span></div>
          <div class="mock-body"><div class="mock-eyebrow">Neighbourhood guide</div><div class="mock-title">Find your place<br>in Mumbai.</div><div class="mock-sub">Explore rental options across the city's neighbourhoods.</div><div class="mock-hero-photo"></div><div class="mock-stats"><div class="mock-stat"><b>1 BHK</b><span>Compact</span></div><div class="mock-stat"><b>2 BHK</b><span>Flexible</span></div><div class="mock-stat"><b>3 BHK</b><span>Spacious</span></div></div></div>
        </div>
        <div class="mock-panel center">
          <div class="mock-topbar"><i class="mock-dot"></i><i class="mock-dot"></i><i class="mock-dot"></i><span class="mock-brand">ESTATEIQ · MUMBAI</span></div>
          <div class="mock-body"><div class="mock-eyebrow">Mumbai property intelligence</div><div class="mock-title">A smarter way to<br>explore real estate.</div><div class="mock-sub">Rental listings and transparent investment scenarios, all in one place.</div><div class="mock-hero-photo"></div><div class="mock-stats"><div class="mock-stat"><b>Explore</b><span>Listings</span></div><div class="mock-stat"><b>Compare</b><span>Localities</span></div><div class="mock-stat"><b>Evaluate</b><span>Returns*</span></div></div><span class="mock-chip">DATA-LED DISCOVERY</span></div>
        </div>
        <div class="mock-panel right">
          <div class="mock-topbar"><i class="mock-dot"></i><i class="mock-dot"></i><i class="mock-dot"></i><span class="mock-brand">INVESTMENT LAB</span></div>
          <div class="mock-body"><div class="mock-eyebrow">Investment snapshot</div><div class="mock-title">See beyond<br>the listing.</div><div class="mock-sub">Compare rental yield and test your own assumptions.</div><div class="mock-listing"><div class="mock-thumb"></div><div><b>Locality comparison</b><span>Median rent · Estimated yield</span></div></div><div class="mock-line"></div><div class="mock-line short"></div><div class="mock-stats"><div class="mock-stat"><b>Rent</b><span>Monthly</span></div><div class="mock-stat"><b>Yield</b><span>Estimated</span></div><div class="mock-stat"><b>ROI</b><span>Scenario</span></div></div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    a,b=st.columns([1,1])
    with a:
        if st.button('Explore properties  →',type='primary',use_container_width=True): go('Explore listings')
    with b:
        if st.button('Open investment lab  ↗',use_container_width=True): go('Investment lab')
    st.markdown('<div style="height:20px"></div><div class="eyebrow">A clearer way to evaluate property</div><div class="section-title">Your property research, all in one place.</div><div class="section-sub">Move from browsing listings to comparing the financial assumptions behind a potential investment.</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    cards=[('⌕','Explore listings','Filter the dataset by locality, rent, and bedroom count to find relevant properties.'),('↗','Investment lab','Estimate rental yield, net income, payback period, and scenario-based returns.'),('▥','Market insights','Compare neighbourhood rent and property-size statistics using clear visualizations.')]
    for col,(icon,title,desc) in zip([c1,c2,c3],cards):
        with col:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown('<div style="height:30px"></div><div class="eyebrow">The dataset at a glance</div><div class="section-title">Mumbai rental market snapshot</div>',unsafe_allow_html=True)
    d=calculate(data)
    m1,m2,m3,m4=st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Listings analysed</div><div class="metric-value">{len(d):,}</div><div class="metric-note">After baseline quality checks</div></div>',unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Median monthly rent</div><div class="metric-value">₹{d["Monthly Rent (₹)"].median():,.0f}</div><div class="metric-note">Across included listings</div></div>',unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Median property size</div><div class="metric-value">{d["Area (sq ft)"].median():,.0f} sq ft</div><div class="metric-note">Parsed from source records</div></div>',unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Median estimated net yield</div><div class="metric-value">{d["Net Yield (%)"].median():.2f}%</div><div class="metric-note">Assumption-based estimate*</div></div>',unsafe_allow_html=True)
    st.caption('*Purchase price is estimated using the sidebar assumption; yields are not verified market returns.')
    st.markdown('<div class="footer">EstateIQ · Built by Ananya Terwadkar · Scenario outputs are estimates, not financial advice.</div>',unsafe_allow_html=True)

elif page=='Explore listings':
    st.markdown('<div class="eyebrow">PROPERTY DISCOVERY</div><div class="section-title">Explore Mumbai listings</div><div class="section-sub">Use filters to narrow the dataset, then inspect listing-level rent and estimated yield.</div>',unsafe_allow_html=True)
    f1,f2,f3=st.columns([2,1,1])
    with f1: locs=sorted(data['Locality'].dropna().unique()); chosen=st.multiselect('Neighbourhood / locality',locs,placeholder='All localities')
    with f2: bhks=sorted(int(v) for v in data['BHK number'].dropna().unique() if v>=0); chosen_bhk=st.multiselect('Bedrooms (BHK)',bhks,placeholder='All BHK')
    with f3:
        maxrent=int(min(1000000,max(50000,data['Monthly Rent (₹)'].quantile(.98))))
        rent_limit=st.slider('Monthly rent ceiling (₹)',min_value=5000,max_value=maxrent,value=maxrent,step=5000)
    x=data.copy()
    if chosen: x=x[x['Locality'].isin(chosen)]
    if chosen_bhk: x=x[x['BHK number'].isin(chosen_bhk)]
    x=x[x['Monthly Rent (₹)']<=rent_limit]
    x=calculate(x)
    st.write(f'**{len(x):,}** listings match your filters')
    if x.empty: st.info('No records match these filters. Clear a filter or raise the rent ceiling.')
    else:
        cols=['Title','Locality','BHK number','Area (sq ft)','Monthly Rent (₹)','Furnished','Estimated Purchase Price (₹)','Gross Yield (%)','Net Yield (%)']
        display=x[cols].sort_values('Net Yield (%)',ascending=False)
        st.dataframe(display,hide_index=True,use_container_width=True,column_config={'Monthly Rent (₹)':st.column_config.NumberColumn(format='₹%.0f'),'Estimated Purchase Price (₹)':st.column_config.NumberColumn(format='₹%.0f'),'Gross Yield (%)':st.column_config.NumberColumn(format='%.2f%%'),'Net Yield (%)':st.column_config.NumberColumn(format='%.2f%%')})
        st.download_button('⬇ Download filtered listings CSV',display.to_csv(index=False).encode('utf-8'),'estateiq_filtered_listings.csv','text/csv')

elif page=='Investment lab':
    st.markdown('<div class="eyebrow">INVESTMENT MODELLING</div><div class="section-title">Investment lab</div><div class="section-sub">Stress-test a simple rental investment with explicit assumptions. These are estimates, not a valuation.</div>',unsafe_allow_html=True)
    x=calculate(data)
    min_listings=st.slider('Minimum listings per locality for comparison',1,20,5)
    stats=x.groupby('Locality').agg(Listings=('Title','size'),MedianRent=('Monthly Rent (₹)','median'),MedianArea=('Area (sq ft)','median'),MedianGrossYield=('Gross Yield (%)','median'),MedianNetYield=('Net Yield (%)','median'),MedianPayback=('Payback Period (years)','median')).reset_index()
    stats=stats[stats['Listings']>=min_listings].sort_values('MedianNetYield',ascending=False)
    top=stats.head(15)
    k1,k2,k3=st.columns(3)
    with k1: st.metric('Median net rental yield',f'{x["Net Yield (%)"].median():.2f}%')
    with k2: st.metric('Median annual net rent',f'₹{x["Net Annual Rent (₹)"].median():,.0f}')
    with k3: st.metric('Median payback period',f'{x["Payback Period (years)"].median():.1f} years')
    left,right=st.columns(2)
    with left: st.plotly_chart(style_chart(px.bar(top.sort_values('MedianNetYield'),x='MedianNetYield',y='Locality',orientation='h',title='Localities by median estimated net yield',labels={'MedianNetYield':'Net yield (%)','Locality':''},color='MedianNetYield',color_continuous_scale=['#d7e4d6','#477568'])),use_container_width=True)
    with right: st.plotly_chart(style_chart(px.scatter(x.sample(min(1200,len(x)),random_state=7),x='Estimated Purchase Price (₹)',y='Monthly Rent (₹)',color='Locality',hover_data=['Title','Net Yield (%)'],title='Estimated purchase price vs advertised rent',opacity=.72)),use_container_width=True)
    st.markdown('### Locality comparison')
    st.dataframe(stats.rename(columns={'MedianRent':'Median monthly rent (₹)','MedianArea':'Median area (sq ft)','MedianGrossYield':'Median gross yield (%)','MedianNetYield':'Median net yield (%)','MedianPayback':'Median payback (years)'}),hide_index=True,use_container_width=True)
    st.info('Important: purchase price = parsed area × assumed price per sq ft. Rent may be an asking price; there are no verified individual sale prices in this dataset. Net yield excludes financing, tax, major repairs, and resale costs.')

elif page=='Market insights':
    st.markdown('<div class="eyebrow">MARKET INTELLIGENCE</div><div class="section-title">Market insights</div><div class="section-sub">Descriptive statistics from the supplied Mumbai listing dataset. These charts describe the data; they do not forecast future prices.</div>',unsafe_allow_html=True)
    x=calculate(data)
    a,b=st.columns(2)
    with a: st.plotly_chart(style_chart(px.histogram(x,x='Monthly Rent (₹)',nbins=45,title='Distribution of advertised monthly rent',labels={'Monthly Rent (₹)':'Monthly rent (₹)'},color_discrete_sequence=['#477568'])),use_container_width=True)
    with b: st.plotly_chart(style_chart(px.box(x,x='BHK number',y='Monthly Rent (₹)',title='Rent distribution by BHK',labels={'BHK number':'Bedrooms (BHK)','Monthly Rent (₹)':'Monthly rent (₹)'},color='BHK number',color_discrete_sequence=['#c8754d','#8e9f79','#6d8790','#d6b887'])),use_container_width=True)
    locstats=x.groupby('Locality').agg(Listings=('Title','size'),MedianRent=('Monthly Rent (₹)','median'),MedianArea=('Area (sq ft)','median'),MedianYield=('Net Yield (%)','median')).reset_index().query('Listings >= 5').sort_values('MedianRent',ascending=False)
    st.plotly_chart(style_chart(px.bar(locstats.head(25),x='Locality',y='MedianRent',title='25 localities with highest median advertised rent (minimum 5 listings)',labels={'MedianRent':'Median monthly rent (₹)','Locality':'Locality'},color='MedianRent',color_continuous_scale=['#d7e4d6','#477568'])),use_container_width=True)
    st.markdown('### Statistical summary')
    st.dataframe(x[['Monthly Rent (₹)','Area (sq ft)','BHK number','Gross Yield (%)','Net Yield (%)']].describe().round(2),use_container_width=True)
    st.caption('The source contains listing data, not a complete census of properties or verified transaction data. Area values are parsed from the first numeric value in the source field.')

st.markdown('<div class="footer">EstateIQ Mumbai · Built by Ananya Terwadkar · Data caveat: outputs depend on assumptions and source listing quality.</div>',unsafe_allow_html=True)
