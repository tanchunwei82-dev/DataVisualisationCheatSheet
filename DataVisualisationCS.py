import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Visualisation Cheat Sheet",
    page_icon="📊",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────────────────────────
if st.session_state.get('showcase', False):
    st.title("📐 Visualisation to Hypothesis")
    st.markdown("*Each chart supports a specific analytical claim — the foundation of data storytelling.*")
else:
    st.title("📊 Data Visualisation Cheat Sheet")
    st.markdown("*A personal reference guide by Tan Chun Wei — tanchunwei.com*")
st.divider()

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    perf = pd.read_csv('performance_logs.csv')
    perf['Month'] = pd.to_datetime(perf['Month'])
    assets = pd.read_csv('assets.csv')
    risks = pd.read_csv('risk_register.csv')
    maint = pd.read_csv('maintenance_logs.csv')
    return perf, assets, risks, maint

try:
    perf_df, assets_df, risks_df, maint_df = load_data()
except:
    st.warning("⚠️ CSV files not found. Using sample data instead.")
    np.random.seed(42)
    months = pd.date_range('2024-01-01', periods=12, freq='MS')
    assets_list = ['ASSET-001', 'ASSET-002', 'ASSET-003', 'ASSET-004']
    perf_df = pd.DataFrame([
        {'Month': m, 'Asset_ID': a,
         'Actual_Yield_MWh': np.random.normal(100, 15),
         'Expected_Yield_MWh': 100,
         'Performance_Ratio_Pct': np.random.normal(95, 8),
         'Irradiation_kWh_m2': np.random.normal(130, 10),
         'Downtime_Hours': np.random.randint(0, 20)}
        for m in months for a in assets_list
    ])

# ── Session State ─────────────────────────────────────────────────────────────
if 'showcase' not in st.session_state:
    st.session_state.showcase = False
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = "📈 Line Chart"

def on_chart_change():
    st.session_state.showcase = False

def on_showcase_change():
    if st.session_state.showcase:
        st.session_state.chart_type = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("📚 Chart Types")
chart_type = st.sidebar.radio(
    "Select a chart to explore:",
    ["📈 Line Chart", "📊 Bar Chart", "📉 Histogram",
     "🔵 Scatter Plot", "📦 Box Plot", "🟥 Heatmap", "🥧 Pie Chart"],
    index=0 if not st.session_state.showcase else None,
    on_change=on_chart_change,
    key="chart_type"
)

st.sidebar.divider()
st.sidebar.markdown("**✨ Want to see more?**")
showcase = st.sidebar.checkbox(
    "📐 Showcase — Visualisation to Hypothesis",
    key="showcase",
    on_change=on_showcase_change
)
show_hypothesis = "📐 Visualisation to Hypothesis" if showcase else "None"

st.sidebar.divider()
st.sidebar.markdown("**📋 Quick Reference**")
st.sidebar.markdown("""
| Chart | Best For |
|---|---|
| 📈 Line | Trends over time |
| 📊 Bar | Compare categories |
| 📉 Histogram | Distributions |
| 🔵 Scatter | Correlations |
| 📦 Box | Spread & outliers |
| 🟥 Heatmap | Patterns in matrix |
| 🥧 Pie | Part of whole |
""")

# ── 1. LINE CHART ─────────────────────────────────────────────────────────────
if chart_type == "📈 Line Chart" and show_hypothesis == "None":
    st.header("📈 Line Chart")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **When to use:**
        - Show trends over time
        - Compare multiple series
        - Continuous data

        **Best for:** Time series, performance tracking
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — x-axis column
        - `y` — y-axis column
        - `color` — group by category
        - `markers=True` — show data points
        """)
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
    with tab1:
        st.code("""
fig = px.line(df, x='Month', y='Actual_Yield_MWh',
              color='Asset_ID', markers=True,
              title='Monthly Energy Yield by Asset')
fig.show()
        """, language='python')
        fig = px.line(perf_df, x='Month', y='Actual_Yield_MWh',
                      color='Asset_ID', markers=True,
                      title='Monthly Energy Yield by Asset (2024)',
                      labels={'Actual_Yield_MWh': 'Yield (MWh)'})
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.code("""
monthly = df.groupby('Month')['Actual_Yield_MWh'].sum()
monthly.plot(kind='line', marker='o')
plt.title('Total Monthly Yield')
plt.show()
        """, language='python')
        fig2, ax = plt.subplots(figsize=(10, 4))
        perf_df.groupby('Month')['Actual_Yield_MWh'].sum().plot(kind='line', marker='o', ax=ax, color='steelblue')
        ax.set_title('Total Monthly Yield (2024)')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig2)

# ── 2. BAR CHART ──────────────────────────────────────────────────────────────
elif chart_type == "📊 Bar Chart" and show_hypothesis == "None":
    st.header("📊 Bar Chart")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **When to use:**
        - Compare values across categories
        - Show rankings
        - Group comparisons

        **Best for:** Asset comparisons, performance rankings
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — categories
        - `y` — values
        - `barmode` — 'group' or 'stack'
        - `color` — colour by category
        """)
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
    with tab1:
        st.code("""
avg = df.groupby('Asset_ID')['Actual_Yield_MWh'].mean().reset_index()
fig = px.bar(avg, x='Asset_ID', y='Actual_Yield_MWh',
             color='Asset_ID', title='Average Monthly Yield by Asset')
fig.show()
        """, language='python')
        avg = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].mean().reset_index()
        fig = px.bar(avg, x='Asset_ID', y='Actual_Yield_MWh', color='Asset_ID',
                     title='Average Monthly Yield by Asset',
                     labels={'Actual_Yield_MWh': 'Avg Yield (MWh)'})
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.code("""
df.groupby('Asset_ID')['Actual_Yield_MWh'].mean().plot(kind='bar', rot=0)
plt.title('Average Monthly Yield by Asset')
plt.show()
        """, language='python')
        fig2, ax = plt.subplots(figsize=(8, 4))
        perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].mean().plot(kind='bar', rot=0, ax=ax, color='steelblue')
        ax.set_title('Average Monthly Yield by Asset')
        plt.tight_layout()
        st.pyplot(fig2)

# ── 3. HISTOGRAM ──────────────────────────────────────────────────────────────
elif chart_type == "📉 Histogram" and show_hypothesis == "None":
    st.header("📉 Histogram")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **When to use:**
        - Distribution of a single variable
        - Spread and skewness
        - Identifying outliers

        **Best for:** Performance ratio distribution
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — column to distribute
        - `nbins` — number of bins
        - `color` — group by category
        """)
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
    with tab1:
        st.code("""
fig = px.histogram(df, x='Performance_Ratio_Pct',
                   nbins=20, color='Asset_ID',
                   title='Distribution of Performance Ratio')
fig.show()
        """, language='python')
        fig = px.histogram(perf_df, x='Performance_Ratio_Pct', nbins=20, color='Asset_ID',
                           title='Distribution of Performance Ratio (%)',
                           labels={'Performance_Ratio_Pct': 'Performance Ratio (%)'})
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.code("""
df['Performance_Ratio_Pct'].plot(kind='hist', bins=20)
plt.title('Distribution of Performance Ratio')
plt.show()
        """, language='python')
        fig2, ax = plt.subplots(figsize=(8, 4))
        perf_df['Performance_Ratio_Pct'].plot(kind='hist', bins=20, ax=ax, color='steelblue', edgecolor='white')
        ax.set_title('Distribution of Performance Ratio (%)')
        plt.tight_layout()
        st.pyplot(fig2)

# ── 4. SCATTER PLOT ───────────────────────────────────────────────────────────
elif chart_type == "🔵 Scatter Plot" and show_hypothesis == "None":
    st.header("🔵 Scatter Plot")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **When to use:**
        - Relationship between two variables
        - Correlations
        - Outlier detection

        **Best for:** Actual vs Expected yield
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — x-axis variable
        - `y` — y-axis variable
        - `color` — group by category
        - `trendline` — regression line
        """)
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
    with tab1:
        st.code("""
fig = px.scatter(df, x='Expected_Yield_MWh', y='Actual_Yield_MWh',
                 color='Asset_ID', trendline='ols',
                 title='Actual vs Expected Yield')
fig.show()
        """, language='python')
        fig = px.scatter(perf_df, x='Expected_Yield_MWh', y='Actual_Yield_MWh',
                         color='Asset_ID', trendline='ols',
                         title='Actual vs Expected Yield by Asset')
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.code("""
df.plot(kind='scatter', x='Expected_Yield_MWh',
        y='Actual_Yield_MWh', alpha=0.6)
plt.title('Actual vs Expected Yield')
plt.show()
        """, language='python')
        fig2, ax = plt.subplots(figsize=(8, 4))
        perf_df.plot(kind='scatter', x='Expected_Yield_MWh', y='Actual_Yield_MWh', ax=ax, alpha=0.6, color='steelblue')
        ax.set_title('Actual vs Expected Yield')
        plt.tight_layout()
        st.pyplot(fig2)

# ── 5. BOX PLOT ───────────────────────────────────────────────────────────────
elif chart_type == "📦 Box Plot" and show_hypothesis == "None":
    st.header("📦 Box Plot")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **When to use:**
        - Spread and distribution
        - Compare groups
        - Identify outliers

        **Best for:** Performance ratio spread per asset
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — category grouping
        - `y` — values
        - `points` — 'all', 'outliers', False
        - `color` — colour by group
        """)
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
    with tab1:
        st.code("""
fig = px.box(df, x='Asset_ID', y='Performance_Ratio_Pct',
             color='Asset_ID', points='all',
             title='Performance Ratio by Asset')
fig.show()
        """, language='python')
        fig = px.box(perf_df, x='Asset_ID', y='Performance_Ratio_Pct',
                     color='Asset_ID', points='all',
                     title='Performance Ratio Distribution by Asset')
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.code("""
df.boxplot(column='Performance_Ratio_Pct', by='Asset_ID')
plt.title('Performance Ratio by Asset')
plt.show()
        """, language='python')
        fig2, ax = plt.subplots(figsize=(8, 4))
        perf_df.boxplot(column='Performance_Ratio_Pct', by='Asset_ID', ax=ax)
        ax.set_title('Performance Ratio by Asset')
        plt.suptitle('')
        plt.tight_layout()
        st.pyplot(fig2)

# ── 6. HEATMAP ────────────────────────────────────────────────────────────────
elif chart_type == "🟥 Heatmap" and show_hypothesis == "None":
    st.header("🟥 Heatmap")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **When to use:**
        - Patterns in a matrix
        - Two categorical variables
        - Correlation matrices

        **Best for:** Monthly performance by asset
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `color_continuous_scale` — colour palette
        - `text_auto` — show values in cells
        - `aspect` — cell shape
        """)
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
    perf_df['Month_Label'] = perf_df['Month'].dt.strftime('%b')
    pivot = perf_df.pivot_table(values='Performance_Ratio_Pct',
                                index='Asset_ID', columns='Month_Label', aggfunc='mean')
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    pivot = pivot[[m for m in month_order if m in pivot.columns]]
    with tab1:
        st.code("""
pivot = df.pivot_table(values='Performance_Ratio_Pct',
                       index='Asset_ID',
                       columns=df['Month'].dt.strftime('%b'),
                       aggfunc='mean')
fig = px.imshow(pivot, color_continuous_scale='RdYlGn',
                text_auto='.1f', title='Performance Ratio Heatmap')
fig.show()
        """, language='python')
        fig = px.imshow(pivot, color_continuous_scale='RdYlGn',
                        text_auto='.1f', aspect='auto',
                        title='Performance Ratio Heatmap by Asset & Month (%)')
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.code("""
fig, ax = plt.subplots(figsize=(12, 4))
im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto')
plt.colorbar(im)
plt.title('Performance Ratio Heatmap')
plt.show()
        """, language='python')
        fig2, ax = plt.subplots(figsize=(12, 3))
        im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto')
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_xticklabels(pivot.columns)
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels(pivot.index)
        plt.colorbar(im, ax=ax)
        ax.set_title('Performance Ratio Heatmap (%)')
        plt.tight_layout()
        st.pyplot(fig2)

# ── 7. PIE CHART ──────────────────────────────────────────────────────────────
elif chart_type == "🥧 Pie Chart" and show_hypothesis == "None":
    st.header("🥧 Pie Chart")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **When to use:**
        - Part-of-whole relationships
        - Proportions (< 6 categories)

        **Best for:** Yield share by asset
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `values` — numeric values
        - `names` — category labels
        - `hole` — donut chart (0–1)
        - `pull` — explode a slice
        """)
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
    with tab1:
        st.code("""
total = df.groupby('Asset_ID')['Actual_Yield_MWh'].sum().reset_index()
fig = px.pie(total, values='Actual_Yield_MWh', names='Asset_ID',
             title='Total Yield Share by Asset', hole=0.4)
fig.show()
        """, language='python')
        total_yield = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].sum().reset_index()
        fig = px.pie(total_yield, values='Actual_Yield_MWh', names='Asset_ID',
                     title='Total Yield Share by Asset (2024)', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.code("""
total = df.groupby('Asset_ID')['Actual_Yield_MWh'].sum()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(total.values, labels=total.index, autopct='%1.1f%%')
plt.show()
        """, language='python')
        total = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].sum()
        fig2, ax = plt.subplots(figsize=(6, 6))
        ax.pie(total.values, labels=total.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Total Yield Share by Asset (2024)')
        plt.tight_layout()
        st.pyplot(fig2)

# ── SHOWCASE: HYPOTHESIS TESTING ──────────────────────────────────────────────
if show_hypothesis == "📐 Visualisation to Hypothesis":
    st.header("📐 Visualisation to Hypothesis")
    st.markdown("*Each chart below supports a specific analytical claim — the foundation of data storytelling.*")
    st.divider()

    # Hypothesis 1
    st.subheader("Hypothesis 1 — ASSET-004 Underperforms in Q3")
    st.info("💡 **Claim:** Johor Carport (ASSET-004) consistently underperforms during July–September due to maintenance issues.")
    perf_df['Quarter'] = perf_df['Month'].dt.quarter
    fig1 = px.line(perf_df, x='Month', y='Performance_Ratio_Pct', color='Asset_ID', markers=True,
                   title='Monthly Performance Ratio — Q3 Underperformance Visible',
                   labels={'Performance_Ratio_Pct': 'Performance Ratio (%)'})
    fig1.add_vrect(x0="2024-07-01", x1="2024-09-30", fillcolor="red", opacity=0.1,
                   layer="below", line_width=0, annotation_text="Q3", annotation_position="top left")
    st.plotly_chart(fig1, use_container_width=True)
    asset4 = perf_df[perf_df['Asset_ID'] == 'ASSET-004']
    q3_avg = asset4[asset4['Quarter'] == 3]['Performance_Ratio_Pct'].mean()
    non_q3_avg = asset4[asset4['Quarter'] != 3]['Performance_Ratio_Pct'].mean()
    col1, col2 = st.columns(2)
    col1.metric("ASSET-004 Q3 Average PR", f"{q3_avg:.1f}%")
    col2.metric("ASSET-004 Non-Q3 Average PR", f"{non_q3_avg:.1f}%", delta=f"{non_q3_avg - q3_avg:.1f}% higher")
    st.success("✅ **Conclusion:** ASSET-004 shows significantly lower performance ratio in Q3 (Jul–Sep), consistent with maintenance activity during this period.")
    st.divider()

    # Hypothesis 2
    st.subheader("Hypothesis 2 — Higher Irradiation = Higher Yield")
    st.info("💡 **Claim:** There is a positive correlation between monthly irradiation and actual energy yield.")
    fig2 = px.scatter(perf_df, x='Irradiation_kWh_m2', y='Actual_Yield_MWh',
                      color='Asset_ID', trendline='ols',
                      title='Irradiation vs Actual Yield — Positive Correlation',
                      labels={'Irradiation_kWh_m2': 'Irradiation (kWh/m²)', 'Actual_Yield_MWh': 'Actual Yield (MWh)'})
    st.plotly_chart(fig2, use_container_width=True)
    st.success("✅ **Conclusion:** A clear positive correlation exists — higher solar irradiation consistently produces more energy output across all APAC sites.")
    st.divider()

    # Hypothesis 3
    st.subheader("Hypothesis 3 — Yield Variance is Worst in Q3")
    st.info("💡 **Claim:** Yield variance (actual vs expected) is most negative during Q3 across all assets.")
    perf_df['Yield_Variance'] = perf_df['Actual_Yield_MWh'] - perf_df['Expected_Yield_MWh']
    perf_df['Month_Label'] = perf_df['Month'].dt.strftime('%b')
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    pivot_var = perf_df.pivot_table(values='Yield_Variance', index='Asset_ID', columns='Month_Label', aggfunc='mean')
    pivot_var = pivot_var[[m for m in month_order if m in pivot_var.columns]]
    fig3 = px.imshow(pivot_var, title='Yield Variance Heatmap by Asset & Month (MWh)',
                     color_continuous_scale='RdYlGn', text_auto='.1f',
                     aspect='auto', color_continuous_midpoint=0)
    st.plotly_chart(fig3, use_container_width=True)
    st.success("✅ **Conclusion:** Negative yield variance (red) is concentrated in Q3 (Jul–Sep), particularly for ASSET-004 — confirming Q3 is the most challenging performance period.")
    st.divider()

    # Hypothesis 4
    st.subheader("Hypothesis 4 — Portfolio Yield is Dominated by Largest Asset")
    st.info("💡 **Claim:** ASSET-001 (Sabah, 13.45 MWp) contributes the majority of total portfolio yield due to its larger installed capacity.")
    total_yield = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].sum().reset_index()
    col1, col2 = st.columns(2)
    with col1:
        fig4a = px.pie(total_yield, values='Actual_Yield_MWh', names='Asset_ID',
                       title='Total Yield Share by Asset (2024)', hole=0.4)
        st.plotly_chart(fig4a, use_container_width=True)
    with col2:
        cap_df = pd.DataFrame({'Asset_ID': ['ASSET-001','ASSET-002','ASSET-003','ASSET-004'],
                               'Capacity_MWp': [13.45, 2.83, 4.20, 1.80]})
        fig4b = px.bar(cap_df, x='Asset_ID', y='Capacity_MWp',
                       title='Installed Capacity by Asset (MWp)', color='Asset_ID')
        st.plotly_chart(fig4b, use_container_width=True)
    st.success("✅ **Conclusion:** ASSET-001 dominates portfolio yield — directly proportional to its installed capacity advantage over the other three APAC sites.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align: center; color: grey; font-size: 14px;'>
Built by Tan Chun Wei | tanchunwei.com | Data: Simulated APAC Solar Asset Portfolio
</div>
""", unsafe_allow_html=True)
