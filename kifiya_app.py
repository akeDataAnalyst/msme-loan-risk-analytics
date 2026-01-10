#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ==================== CONFIG ====================
st.set_page_config(
    page_title="Kifiya MSME Loan Portfolio Analytics",
    page_icon="https://kifiya.com/wp-content/uploads/2025/03/Kifiya-logo-white.webp",
    layout="wide"
)

# Custom CSS for sticky/fixed header
st.markdown("""
<style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1.5rem 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        z-index: 999;
        border-bottom: 1px solid #e0e0e0;
    }
    .main-content {
        margin-top: 220px;  /* Adjust based on header height */
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOAD FROM CSV ====================
@st.cache_data
def load_data():
    csv_path = 'ethiopian_msme_loans_realistic.csv'
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# ==================== SIDEBAR ====================
st.sidebar.image("https://kifiya.com/wp-content/uploads/2025/03/Kifiya-logo-white.webp", use_column_width=True)
st.sidebar.markdown("### Kifiya Portfolio Dashboard")

st.sidebar.metric("Total Loans", f"{len(df):,}")
st.sidebar.metric("Overall Default Rate", f"{df['default'].mean()*100:.1f}%")
st.sidebar.metric("Agriculture Exposure", f"{df['sector'].str.contains('Agriculture').mean()*100:.0f}%")

# Filters
st.sidebar.markdown("### Filters")
selected_regions = st.sidebar.multiselect(
    "Regions", 
    options=sorted(df['region'].unique()), 
    default=sorted(df['region'].unique())
)
selected_sectors = st.sidebar.multiselect(
    "Sectors", 
    options=sorted(df['sector'].unique()), 
    default=sorted(df['sector'].unique())
)

filtered_df = df[
    df['region'].isin(selected_regions) & 
    df['sector'].isin(selected_sectors)
]

# ==================== FIXED HEADER ====================
with st.container():
    st.markdown('<div class="fixed-header">', unsafe_allow_html=True)
    
    st.markdown("# Kifiya AI-Powered MSME Loan Portfolio Risk Analytics")
    st.markdown("### Realistic Ethiopian Digital Lending Portfolio — Built for Kifiya")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Loans", f"{len(filtered_df):,}")
    with col2:
        st.metric("Total Defaults", filtered_df['default'].sum())
    with col3:
        st.metric("Portfolio Default Rate", f"{filtered_df['default'].mean()*100:.1f}%")
    with col4:
        st.metric("Avg Loan Amount (ETB)", f"{filtered_df['loan_amount_etb'].mean():,.0f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content starts below fixed header
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ==================== DASHBOARD CONTENT ====================

st.subheader("Default Rate by Sector")
sector_risk = (filtered_df.groupby('sector')
               .agg(total=('default', 'count'), defaults=('default', 'sum'))
               .reset_index())
sector_risk['default_rate'] = (sector_risk['defaults'] / sector_risk['total'] * 100).round(1)
sector_risk = sector_risk.sort_values('default_rate', ascending=False)

fig_sector = px.bar(
    sector_risk, 
    x='default_rate', 
    y='sector', 
    orientation='h',
    text='default_rate',
    color='default_rate',
    color_continuous_scale='Reds',
    title="Default Rate by Sector (%)"
)
fig_sector.update_traces(texttemplate='%{text}%')
fig_sector.update_layout(height=500, showlegend=False)
st.plotly_chart(fig_sector, use_container_width=True)

st.subheader("Risk Profile: Defaulted vs Performing Loans")
comparison = filtered_df.groupby('default').agg({
    'income_variability': 'mean',
    'mobile_transactions': 'mean',
    'credit_score': 'mean',
    'loan_amount_etb': 'mean'
}).round(2).reset_index()

comparison_long = pd.melt(comparison, id_vars='default', var_name='metric', value_name='value')
comparison_long['status'] = comparison_long['default'].map({0: 'Performing', 1: 'Defaulted'})

fig_compare = px.bar(
    comparison_long, 
    x='metric', 
    y='value', 
    color='status',
    barmode='group',
    title="Average Risk Metrics: Defaulted vs Performing",
    labels={'value': 'Average Value', 'metric': 'Risk Metric'}
)
st.plotly_chart(fig_compare, use_container_width=True)

st.subheader("Default Rate by Region")
region_risk = (filtered_df.groupby('region')
               .agg(total=('default', 'count'), defaults=('default', 'sum'))
               .reset_index())
region_risk['default_rate'] = (region_risk['defaults'] / region_risk['total'] * 100).round(1)
region_risk = region_risk.sort_values('default_rate', ascending=False)

fig_region = px.bar(
    region_risk,
    x='default_rate',
    y='region',
    orientation='h',
    text='default_rate',
    color='default_rate',
    color_continuous_scale='Oranges',
    title="Default Rate by Region (%)"
)
fig_region.update_traces(texttemplate='%{text}%')
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Data-Driven Recommendations")
st.markdown("""
1. **Agriculture Risk Mitigation**  
   ~67% default rate in smallholder farming — recommend climate-smart insurance, input financing bundles, and enhanced monitoring.

2. **Alternative Data Excellence**  
   Mobile transactions and income variability are the strongest predictors — expand Ascent-like AI scoring for better inclusion without excessive risk.

3. **Proactive Portfolio Management**  
   Identify and engage high-volatility performing loans early to prevent migration to NPLs.

4. **Strategic Diversification**  
   Increase exposure to Digital/Tech and Trade sectors (4–6% defaults) to balance inclusion goals with portfolio health.

5. **Real-Time Deployment Ready**  
   High-AUC predictive model suitable for integration into Efoyta, Michu, and Ansar platforms.
""")

# Close main-content div
st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "**Aklilu  Abera** | **Financial Analyst (Data & Analytics Focus)** >",
    unsafe_allow_html=True
)


# In[ ]:




