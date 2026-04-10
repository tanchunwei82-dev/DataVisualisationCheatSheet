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
    data_loaded = True
except:
    st.warning("⚠️ CSV files not found. Using sample data instead.")
    data_loaded = False
    # Generate sample data if CSVs not available
    np.random.seed(42)
    months = pd.date_range('2024-01-01', periods=12, freq='MS')
    assets_list = ['ASSET-001', 'ASSET-002', 'ASSET-003', 'ASSET-004']
    perf_df = pd.DataFrame([
        {'Month': m, 'Asset_ID': a,
         'Actual_Yield_MWh': np.random.normal(100, 15),
         'Expected_Yield_MWh': 100,
         'Performance_Ratio_Pct': np.random.normal(95, 8),
         'Downtime_Hours': np.random.randint(0, 20)}
        for m in months for a in assets_list
    ])
 
# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("📚 Chart Types")
chart_type = st.sidebar.radio("Select a chart type:", [
    "📈 Line Chart",
    "📊 Bar Chart",
    "📉 Histogram",
    "🔵 Scatter Plot",
    "📦 Box Plot",
    "🟥 Heatmap",
    "🥧 Pie Chart",
])
 
st.sidebar.divider()
st.sidebar.markdown("**Quick Reference**")
st.sidebar.markdown("""
| Chart | Best For |
|---|---|
| Line | Trends over time |
| Bar | Comparisons |
| Histogram | Distributions |
| Scatter | Correlations |
| Box | Spread & outliers |
| Heatmap | Patterns in matrix |
| Pie | Part of whole |
""")
 
# ── Chart Sections ────────────────────────────────────────────────────────────
 
# ── 1. LINE CHART ─────────────────────────────────────────────────────────────
if chart_type == "📈 Line Chart":
    st.header("📈 Line Chart")
 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **When to use:**
        - Show trends over time
        - Compare multiple series over time
        - Continuous data
 
        **Best for:** Time series, performance tracking, yield trends
        """)
 
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — x-axis column
        - `y` — y-axis column
        - `color` — group by category
        - `title` — chart title
        - `markers=True` — show data points
        """)
 
    st.divider()
 
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Pandas/Matplotlib (Static)"])
 
    with tab1:
        st.subheader("Plotly Line Chart")
        st.code("""
import plotly.express as px
 
fig = px.line(df, 
              x='Month', 
              y='Actual_Yield_MWh',
              color='Asset_ID',
              title='Monthly Energy Yield by Asset',
              markers=True,
              labels={'Actual_Yield_MWh': 'Yield (MWh)', 'Month': 'Month'})
fig.show()
        """, language='python')
 
        fig = px.line(perf_df,
                      x='Month',
                      y='Actual_Yield_MWh',
                      color='Asset_ID',
                      title='Monthly Energy Yield by Asset (2024)',
                      markers=True,
                      labels={'Actual_Yield_MWh': 'Yield (MWh)', 'Month': 'Month'})
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.subheader("Pandas/Matplotlib Line Chart")
        st.code("""
import matplotlib.pyplot as plt
 
monthly = df.groupby('Month')['Actual_Yield_MWh'].sum()
monthly.plot(kind='line', marker='o', figsize=(10, 5))
plt.title('Total Monthly Yield')
plt.ylabel('Yield (MWh)')
plt.xlabel('Month')
plt.grid(True)
plt.tight_layout()
plt.show()
        """, language='python')
 
        fig2, ax = plt.subplots(figsize=(10, 4))
        monthly = perf_df.groupby('Month')['Actual_Yield_MWh'].sum()
        monthly.plot(kind='line', marker='o', ax=ax, color='steelblue')
        ax.set_title('Total Monthly Yield (2024)')
        ax.set_ylabel('Yield (MWh)')
        ax.set_xlabel('Month')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig2)
 
# ── 2. BAR CHART ──────────────────────────────────────────────────────────────
elif chart_type == "📊 Bar Chart":
    st.header("📊 Bar Chart")
 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **When to use:**
        - Compare values across categories
        - Show rankings
        - Compare groups side by side
 
        **Best for:** Asset comparisons, performance rankings
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — categories
        - `y` — values
        - `barmode` — 'group' or 'stack'
        - `orientation` — 'v' or 'h'
        - `color` — colour by category
        """)
 
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Pandas/Matplotlib (Static)"])
 
    with tab1:
        st.subheader("Plotly Bar Chart")
        st.code("""
import plotly.express as px
 
avg_yield = df.groupby('Asset_ID')['Actual_Yield_MWh'].mean().reset_index()
 
fig = px.bar(avg_yield,
             x='Asset_ID',
             y='Actual_Yield_MWh',
             title='Average Monthly Yield by Asset',
             color='Asset_ID',
             labels={'Actual_Yield_MWh': 'Avg Yield (MWh)'})
fig.show()
        """, language='python')
 
        avg_yield = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].mean().reset_index()
        fig = px.bar(avg_yield,
                     x='Asset_ID',
                     y='Actual_Yield_MWh',
                     title='Average Monthly Yield by Asset',
                     color='Asset_ID',
                     labels={'Actual_Yield_MWh': 'Avg Yield (MWh)'})
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.subheader("Pandas/Matplotlib Bar Chart")
        st.code("""
avg = df.groupby('Asset_ID')['Actual_Yield_MWh'].mean()
avg.plot(kind='bar', rot=0, figsize=(8, 5), color='steelblue')
plt.title('Average Monthly Yield by Asset')
plt.ylabel('Avg Yield (MWh)')
plt.tight_layout()
plt.show()
        """, language='python')
 
        fig2, ax = plt.subplots(figsize=(8, 4))
        avg = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].mean()
        avg.plot(kind='bar', rot=0, ax=ax, color='steelblue')
        ax.set_title('Average Monthly Yield by Asset')
        ax.set_ylabel('Avg Yield (MWh)')
        plt.tight_layout()
        st.pyplot(fig2)
 
# ── 3. HISTOGRAM ──────────────────────────────────────────────────────────────
elif chart_type == "📉 Histogram":
    st.header("📉 Histogram")
 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **When to use:**
        - Show distribution of a single variable
        - Understand spread and skewness
        - Identify outliers
 
        **Best for:** Performance ratio distribution, yield spread analysis
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — column to distribute
        - `nbins` — number of bins
        - `color` — group by category
        - `bins` — number of bins (matplotlib)
        - `kde` — show density curve
        """)
 
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Pandas/Matplotlib (Static)"])
 
    with tab1:
        st.subheader("Plotly Histogram")
        st.code("""
import plotly.express as px
 
fig = px.histogram(df,
                   x='Performance_Ratio_Pct',
                   nbins=20,
                   title='Distribution of Performance Ratio',
                   color='Asset_ID',
                   labels={'Performance_Ratio_Pct': 'Performance Ratio (%)'})
fig.show()
        """, language='python')
 
        fig = px.histogram(perf_df,
                           x='Performance_Ratio_Pct',
                           nbins=20,
                           title='Distribution of Performance Ratio (%)',
                           color='Asset_ID',
                           labels={'Performance_Ratio_Pct': 'Performance Ratio (%)'})
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.subheader("Pandas/Matplotlib Histogram")
        st.code("""
perf_df['Performance_Ratio_Pct'].plot(kind='hist', bins=20, figsize=(8,5))
plt.title('Distribution of Performance Ratio')
plt.xlabel('Performance Ratio (%)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
        """, language='python')
 
        fig2, ax = plt.subplots(figsize=(8, 4))
        perf_df['Performance_Ratio_Pct'].plot(kind='hist', bins=20, ax=ax, color='steelblue', edgecolor='white')
        ax.set_title('Distribution of Performance Ratio (%)')
        ax.set_xlabel('Performance Ratio (%)')
        ax.set_ylabel('Frequency')
        plt.tight_layout()
        st.pyplot(fig2)
 
# ── 4. SCATTER PLOT ───────────────────────────────────────────────────────────
elif chart_type == "🔵 Scatter Plot":
    st.header("🔵 Scatter Plot")
 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **When to use:**
        - Show relationship between two variables
        - Identify correlations
        - Spot outliers
 
        **Best for:** Actual vs Expected yield, correlation analysis
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — x-axis variable
        - `y` — y-axis variable
        - `color` — group by category
        - `size` — bubble size
        - `trendline` — add regression line
        """)
 
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Pandas/Matplotlib (Static)"])
 
    with tab1:
        st.subheader("Plotly Scatter Plot")
        st.code("""
import plotly.express as px
 
fig = px.scatter(df,
                 x='Expected_Yield_MWh',
                 y='Actual_Yield_MWh',
                 color='Asset_ID',
                 trendline='ols',
                 title='Actual vs Expected Yield',
                 labels={
                     'Expected_Yield_MWh': 'Expected Yield (MWh)',
                     'Actual_Yield_MWh': 'Actual Yield (MWh)'
                 })
fig.show()
        """, language='python')
 
        fig = px.scatter(perf_df,
                         x='Expected_Yield_MWh',
                         y='Actual_Yield_MWh',
                         color='Asset_ID',
                         trendline='ols',
                         title='Actual vs Expected Yield by Asset',
                         labels={
                             'Expected_Yield_MWh': 'Expected Yield (MWh)',
                             'Actual_Yield_MWh': 'Actual Yield (MWh)'
                         })
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.subheader("Pandas/Matplotlib Scatter Plot")
        st.code("""
perf_df.plot(kind='scatter',
             x='Expected_Yield_MWh',
             y='Actual_Yield_MWh',
             figsize=(8,5), alpha=0.6)
plt.title('Actual vs Expected Yield')
plt.tight_layout()
plt.show()
        """, language='python')
 
        fig2, ax = plt.subplots(figsize=(8, 4))
        perf_df.plot(kind='scatter',
                     x='Expected_Yield_MWh',
                     y='Actual_Yield_MWh',
                     ax=ax, alpha=0.6, color='steelblue')
        ax.set_title('Actual vs Expected Yield')
        plt.tight_layout()
        st.pyplot(fig2)
 
# ── 5. BOX PLOT ───────────────────────────────────────────────────────────────
elif chart_type == "📦 Box Plot":
    st.header("📦 Box Plot")
 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **When to use:**
        - Show spread and distribution
        - Compare distributions across groups
        - Identify outliers visually
 
        **Best for:** Performance ratio spread per asset, downtime distribution
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `x` — category grouping
        - `y` — values to distribute
        - `color` — colour by group
        - `points` — 'all', 'outliers', False
        - `notched` — show confidence interval
        """)
 
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Pandas/Matplotlib (Static)"])
 
    with tab1:
        st.subheader("Plotly Box Plot")
        st.code("""
import plotly.express as px
 
fig = px.box(df,
             x='Asset_ID',
             y='Performance_Ratio_Pct',
             color='Asset_ID',
             points='all',
             title='Performance Ratio Distribution by Asset')
fig.show()
        """, language='python')
 
        fig = px.box(perf_df,
                     x='Asset_ID',
                     y='Performance_Ratio_Pct',
                     color='Asset_ID',
                     points='all',
                     title='Performance Ratio Distribution by Asset')
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.subheader("Pandas/Matplotlib Box Plot")
        st.code("""
perf_df.boxplot(column='Performance_Ratio_Pct',
                by='Asset_ID',
                figsize=(8, 5))
plt.title('Performance Ratio by Asset')
plt.suptitle('')
plt.tight_layout()
plt.show()
        """, language='python')
 
        fig2, ax = plt.subplots(figsize=(8, 4))
        perf_df.boxplot(column='Performance_Ratio_Pct', by='Asset_ID', ax=ax)
        ax.set_title('Performance Ratio by Asset')
        plt.suptitle('')
        plt.tight_layout()
        st.pyplot(fig2)
 
# ── 6. HEATMAP ────────────────────────────────────────────────────────────────
elif chart_type == "🟥 Heatmap":
    st.header("🟥 Heatmap")
 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **When to use:**
        - Show patterns in a matrix
        - Visualise correlations
        - Compare two categorical variables
 
        **Best for:** Monthly performance by asset, correlation matrix
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `z` — values to colour
        - `x` — x-axis categories
        - `y` — y-axis categories
        - `color_continuous_scale` — colour palette
        - `text_auto` — show values in cells
        """)
 
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
 
    with tab1:
        st.subheader("Plotly Heatmap")
        st.code("""
import plotly.express as px
 
pivot = df.pivot_table(
    values='Performance_Ratio_Pct',
    index='Asset_ID',
    columns=df['Month'].dt.strftime('%b'),
    aggfunc='mean'
)
 
fig = px.imshow(pivot,
                title='Performance Ratio Heatmap by Asset & Month',
                color_continuous_scale='RdYlGn',
                text_auto='.1f')
fig.show()
        """, language='python')
 
        perf_df['Month_Label'] = perf_df['Month'].dt.strftime('%b')
        pivot = perf_df.pivot_table(
            values='Performance_Ratio_Pct',
            index='Asset_ID',
            columns='Month_Label',
            aggfunc='mean'
        )
        month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        pivot = pivot[[m for m in month_order if m in pivot.columns]]
 
        fig = px.imshow(pivot,
                        title='Performance Ratio Heatmap by Asset & Month (%)',
                        color_continuous_scale='RdYlGn',
                        text_auto='.1f',
                        aspect='auto')
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.subheader("Matplotlib Heatmap")
        st.code("""
import matplotlib.pyplot as plt
import numpy as np
 
pivot = df.pivot_table(
    values='Performance_Ratio_Pct',
    index='Asset_ID',
    columns=df['Month'].dt.strftime('%b'),
    aggfunc='mean'
)
 
fig, ax = plt.subplots(figsize=(12, 4))
im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto')
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
plt.colorbar(im)
plt.title('Performance Ratio Heatmap')
plt.tight_layout()
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
elif chart_type == "🥧 Pie Chart":
    st.header("🥧 Pie Chart")
 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **When to use:**
        - Show part-of-whole relationships
        - Compare proportions
        - Limited categories (< 6)
 
        **Best for:** Yield share by asset, downtime proportion
        """)
    with col2:
        st.markdown("""
        **Key parameters:**
        - `values` — numeric values
        - `names` — category labels
        - `hole` — donut chart (0 to 1)
        - `title` — chart title
        - `pull` — explode a slice
        """)
 
    st.divider()
    tab1, tab2 = st.tabs(["🟣 Plotly (Interactive)", "🔵 Matplotlib (Static)"])
 
    with tab1:
        st.subheader("Plotly Pie / Donut Chart")
        st.code("""
import plotly.express as px
 
total_yield = df.groupby('Asset_ID')['Actual_Yield_MWh'].sum().reset_index()
 
fig = px.pie(total_yield,
             values='Actual_Yield_MWh',
             names='Asset_ID',
             title='Total Yield Share by Asset (2024)',
             hole=0.4)  # Remove hole=0.4 for regular pie
fig.show()
        """, language='python')
 
        total_yield = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].sum().reset_index()
        fig = px.pie(total_yield,
                     values='Actual_Yield_MWh',
                     names='Asset_ID',
                     title='Total Yield Share by Asset (2024)',
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.subheader("Matplotlib Pie Chart")
        st.code("""
total = df.groupby('Asset_ID')['Actual_Yield_MWh'].sum()
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(total.values, labels=total.index, autopct='%1.1f%%', startangle=90)
ax.set_title('Total Yield Share by Asset')
plt.tight_layout()
plt.show()
        """, language='python')
 
        total = perf_df.groupby('Asset_ID')['Actual_Yield_MWh'].sum()
        fig2, ax = plt.subplots(figsize=(6, 6))
        ax.pie(total.values, labels=total.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Total Yield Share by Asset (2024)')
        plt.tight_layout()
        st.pyplot(fig2)
 
# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align: center; color: grey; font-size: 14px;'>
Built by Tan Chun Wei | tanchunwei.com | Data: Simulated APAC Solar Asset Portfolio
</div>
""", unsafe_allow_html=True)
