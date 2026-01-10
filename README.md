**AI-Powered MSME Loan Portfolio Risk Analytics Dashboard**

**Description**  
End-to-end analytics application that monitors an Ethiopian MSME loan portfolio, predicts default risks using machine learning, and delivers interactive dashboards. Features real-time user interaction, automated risk alerts, and stakeholder-ready visualizations.

**Problem & Solution**  
High default risk in MSME digital lending — caused by limited collateral, data gaps, and sector volatility (e.g., agriculture) — leads to portfolio imbalances, liquidity strain, and reduced financial inclusion.  
Solution: ML-driven pipeline that ingests, cleans, and models data from diverse sources, predicts default probabilities (Random Forest with AUC-ROC ~0.92), flags anomalies (z-score), and provides dynamic insights. Enables proactive risk mitigation, early high-risk segment identification, and supports Kifiya’s mission of scaling inclusive lending safely.

**Tech Stack**  
- **Python** – Data processing (pandas, NumPy), ML modeling (scikit-learn), automation  
- **MySQL** – Backend database for structured storage & analytical queries  
- **Streamlit** – Interactive web app with filters, real-time predictions & alerts  
- **Plotly/Tableau** – Advanced, embeddable visualizations (heatmaps, sector risk charts)

**Key Recommendations**  
- **Diversify exposure**: Cap agriculture sector at 25% if predicted defaults >15%; shift to low-risk eCommerce/Tech segments (potential 12–18% risk reduction)  
- **Leverage alternative data**: Enhance scoring with mobile transactions & income variability → increase approvals for underserved borrowers by ~20% while controlling defaults (aligns with Kifiya Ascent)  
- **Proactive monitoring**: Set automated alerts for anomalies (e.g., delinquency spikes >5% in a region) → enable quarterly reviews & liquidity optimization
