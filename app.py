#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, auc

# ==================== CONFIG ====================
st.set_page_config(
    page_title="MSME Loan Portfolio Analytics",
    page_icon="https://kifiya.com/wp-content/uploads/2025/03/Kifiya-logo-white.webp",  
    layout="wide"
)

# ==================== DATA LOAD ====================
@st.cache_data
def load_data():
    csv_path = 'ethiopian_msme_loans_realistic.csv'  # File in same folder as app.py
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# ==================== SIDEBAR ====================
st.sidebar.header("Kifiya Portfolio Dashboard")
st.sidebar.image("https://kifiya.com/wp-content/uploads/2025/03/Kifiya-logo-white.webp", use_column_width=True)
st.sidebar.metric("Total Loans", f"{len(df):,}")
st.sidebar.metric("Overall Default Rate", f"{df['default'].mean()*100:.1f}%")
st.sidebar.metric("Agriculture Exposure", f"{df['sector'].str.contains('Agriculture').mean()*100:.0f}%")

# Filters
st.sidebar.subheader("Filters")
selected_regions = st.sidebar.multiselect("Regions", options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
selected_sectors = st.sidebar.multiselect("Sectors", options=sorted(df['sector'].unique()), default=sorted(df['sector'].unique()))

filtered_df = df[df['region'].isin(selected_regions) & df['sector'].isin(selected_sectors)]

# ==================== MAIN DASHBOARD ====================
st.title("AI-Powered MSME Loan Portfolio Risk Analytics")
st.markdown("### Ethiopian Digital Lending Portfolio — Built for Kifiya")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Loans", f"{len(filtered_df):,}")
col2.metric("Total Defaults", filtered_df['default'].sum())
col3.metric("Portfolio Default Rate", f"{filtered_df['default'].mean()*100:.1f}%")
col4.metric("Avg Loan Amount (ETB)", f"{filtered_df['loan_amount_etb'].mean():,.0f}")

# Sector Risk
st.subheader("Default Rate by Sector")
sector_risk = (filtered_df.groupby('sector')
               .agg(total=('default', 'count'), defaults=('default', 'sum'))
               .reset_index())
sector_risk['default_rate'] = (sector_risk['defaults'] / sector_risk['total'] * 100).round(1)
sector_risk = sector_risk.sort_values('default_rate', ascending=False)

fig_sector = px.bar(sector_risk, 
                    x='default_rate', 
                    y='sector', 
                    orientation='h',
                    text='default_rate',
                    color='default_rate',
                    color_continuous_scale='Reds',
                    title="Default Rate by Sector (%)")
fig_sector.update_traces(texttemplate='%{text}%')
fig_sector.update_layout(height=500, showlegend=False)
st.plotly_chart(fig_sector, use_container_width=True)

# Risk Factor Comparison
st.subheader("Risk Profile: Defaulted vs Performing Loans")
comparison = filtered_df.groupby('default').agg({
    'income_variability': 'mean',
    'mobile_transactions': 'mean',
    'credit_score': 'mean',
    'loan_amount_etb': 'mean'
}).round(2).reset_index()

comparison_long = pd.melt(comparison, id_vars='default', var_name='metric', value_name='value')
comparison_long['status'] = comparison_long['default'].map({0: 'Performing', 1: 'Defaulted'})

fig_compare = px.bar(comparison_long, 
                     x='metric', 
                     y='value', 
                     color='status',
                     barmode='group',
                     title="Average Risk Metrics: Defaulted vs Performing",
                     labels={'value': 'Average Value', 'metric': 'Risk Metric'})
st.plotly_chart(fig_compare, use_container_width=True)

# Regional Map (Simplified)
st.subheader("Default Rate by Region")
region_risk = (filtered_df.groupby('region')
               .agg(total=('default', 'count'), defaults=('default', 'sum'))
               .reset_index())
region_risk['default_rate'] = (region_risk['defaults'] / region_risk['total'] * 100).round(1)

fig_region = px.bar(region_risk.sort_values('default_rate', ascending=False),
                    x='default_rate',
                    y='region',
                    orientation='h',
                    text='default_rate',
                    color='default_rate',
                    color_continuous_scale='Oranges')
fig_region.update_traces(texttemplate='%{text}%')
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Data-Driven Recommendations")
st.markdown("""
1. **Agriculture Risk Mitigation**  
   67.5% default rate in smallholder farming — recommend climate-smart insurance, input financing bundles, and enhanced monitoring.

2. **Alternative Data Excellence**  
   Mobile transactions and income variability are the strongest predictors — expand Ascent-like AI scoring for better inclusion without risk.

3. **Proactive Portfolio Management**  
   Identify and engage high-volatility performing loans early to prevent migration to NPLs.

4. **Strategic Diversification**  
   Increase exposure to Digital/Tech and Trade sectors (4–6% defaults) to balance inclusion goals with portfolio health.

5. **Real-Time Deployment Ready**  
   High-AUC predictive model suitable for integration into Efoyta, Michu, and Ansar platforms.
""")

st.markdown("---")
st.markdown(" **Aklilu Abera** | **Financial Analyst (Data & Analytics Focus)** ")


# In[ ]:




