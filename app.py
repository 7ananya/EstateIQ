
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
