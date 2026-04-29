import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────
# CSS — dari kode kamu (light theme, pink accent, animasi)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F4F6FB; }

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E4E9F2;
}
section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideRight {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(212, 96, 122, 0.18); }
    50%       { box-shadow: 0 0 0 8px rgba(212, 96, 122, 0); }
}

/* ─── Hero ─── */
.hero {
    background: linear-gradient(135deg, #1E2D5A 0%, #26386E 70%, #2E4080 100%);
    border-radius: 18px;
    padding: 2rem 2rem 1.8rem 2rem;
    margin-bottom: 1.6rem;
    display: flex;
    align-items: center;
    gap: 1.4rem;
    animation: fadeUp 0.6s ease both;
}
.hero-text h1 {
    font-size: 1.65rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0 0 0.25rem;
    letter-spacing: -0.4px;
}
.hero-text p { font-size: 0.83rem; color: #A8B8D8; margin: 0; }
.hero-badge {
    margin-left: auto;
    background: rgba(212, 96, 122, 0.2);
    border: 1px solid rgba(212, 96, 122, 0.4);
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: #F0A0B5;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    flex-shrink: 0;
}

/* ─── Section label ─── */
.sec-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #D4607A;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin: 1.8rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    animation: slideRight 0.5s ease both;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, #E4E9F2, transparent);
}

/* ─── KPI Cards ─── */
.kpi {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    border: 1px solid #E4E9F2;
    box-shadow: 0 2px 10px rgba(30, 45, 90, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: fadeUp 0.5s ease both;
    height: 100%;
}
.kpi:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(30,45,90,0.10); }
.kpi-label {
    font-size: 0.70rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    color: #8A97B5;
    margin-bottom: 0.5rem;
}
.kpi-val {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1E2D5A;
    line-height: 1.1;
    margin-bottom: 0.3rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-sub { font-size: 0.73rem; color: #D4607A; font-weight: 500; }
.kpi-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #D4607A; display: inline-block;
    margin-right: 0.35rem; animation: pulse 2s infinite;
}

/* ─── Chart wrapper ─── */
.chart-wrap {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.2rem 1.3rem 0.4rem;
    border: 1px solid #E4E9F2;
    box-shadow: 0 2px 10px rgba(30, 45, 90, 0.05);
    margin-bottom: 1rem;
    animation: fadeUp 0.55s ease both;
}
.chart-title { font-size: 0.9rem; font-weight: 700; color: #1E2D5A; margin-bottom: 0.1rem; }
.chart-sub   { font-size: 0.75rem; color: #8A97B5; margin-bottom: 0.7rem; }

/* ─── Insight box ─── */
.insight-row { display: flex; gap: 1rem; margin-bottom: 1.6rem; animation: fadeUp 0.6s ease 0.2s both; }
.insight-card {
    flex: 1;
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E4E9F2;
    border-left: 5px solid #D4607A;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 4px 16px rgba(30,45,90,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.insight-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(30,45,90,0.11); }
.insight-card h4 {
    font-size: 0.72rem; font-weight: 700; color: #D4607A;
    text-transform: uppercase; letter-spacing: 1px; margin: 0 0 0.5rem;
}
.insight-num { font-size: 2rem; font-weight: 800; color: #1E2D5A; line-height: 1; margin-bottom: 0.4rem; display: block; }
.insight-card p { font-size: 0.83rem; color: #5A6A8A; margin: 0; line-height: 1.55; }

/* ─── Segment badge ─── */
.seg-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* ─── Sidebar ─── */
.sb-brand {
    text-align: center;
    padding: 0.5rem 0 1.2rem;
    border-bottom: 1px solid #E4E9F2;
    margin-bottom: 1.2rem;
}
.sb-brand-name  { font-size: 0.85rem; font-weight: 700; color: #1E2D5A; display: block; }
.sb-brand-sub   { font-size: 0.68rem; color: #8A97B5; }

/* ─── Streamlit overrides ─── */
label { font-size: 0.78rem !important; color: #3A4A6B !important; font-weight: 600 !important; }
hr    { border: none; border-top: 1px solid #E4E9F2; margin: 1rem 0; }
.streamlit-expanderHeader { font-size: 0.85rem !important; font-weight: 600 !important; color: #1E2D5A !important; }

[data-testid="stTabs"] button                       { color: #8A97B5 !important; font-weight: 600; font-size: 0.82rem; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #1E2D5A !important; border-bottom-color: #D4607A !important; }
[data-testid="stDataFrame"] { border: 1px solid #E4E9F2; border-radius: 10px; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F4F6FB; }
::-webkit-scrollbar-thumb { background: #C8D0E4; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #D4607A; }

/* ─── Hero Logo ─── */
.hero-logo-box {
    flex-shrink: 0;
}
.hero-logo-icon {
    width: 64px;
    height: 64px;
    background: rgba(255,255,255,0.10);
    border: 1.5px solid rgba(255,255,255,0.18);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: pulse 2.8s ease-in-out infinite;
}

.sb-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 0.5rem;
}
.sb-logo svg {
    filter: drop-shadow(0 4px 12px rgba(212, 96, 122, 0.25));
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# COLORS
# ──────────────────────────────────────────────────────────────
NAVY  = "#1E2D5A"
PINK  = "#D4607A"
PINK2 = "#F0AEC0"
SLATE = "#3A4A6B"
LGRAY = "#F4F6FB"
SEG_COLORS = {
    "Champions": "#D4607A",
    "Loyal":     "#2E4080",
    "At Risk":   "#F0A830",
    "Lost":      "#C8D0E4",
}
QUAL = ["#D4607A","#2E5FD4","#2EC4A0","#F0A830","#8E54D4","#28A8C8","#E07040","#50C060"]

def fig_base(fig, h=350, legend=False):
    fig.update_layout(
        height=h,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=SLATE, size=11),
        margin=dict(l=8, r=8, t=8, b=8),
        showlegend=legend,
        legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#E4E9F2",
                    borderwidth=1, font=dict(size=10)),
        xaxis=dict(gridcolor="#EEF1FB", linecolor="#E4E9F2",
                   tickfont=dict(size=10), title_font=dict(size=11, color=SLATE)),
        yaxis=dict(gridcolor="#EEF1FB", linecolor="#E4E9F2",
                   tickfont=dict(size=10), title_font=dict(size=11, color=SLATE))
    )
    return fig

# ──────────────────────────────────────────────────────────────
# DB CONFIG — ganti sesuai punyamu
# ──────────────────────────────────────────────────────────────
DB_URL = "postgresql+psycopg2://postgres:jinggacantik@localhost:5432/dvdrental"

@st.cache_resource
def get_engine():
    return create_engine(DB_URL)

@st.cache_data(ttl=600)
def run_query(sql):
    with get_engine().connect() as conn:
        return pd.read_sql(text(sql), conn)

# ──────────────────────────────────────────────────────────────
# QUERIES
# ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def load_kpi():
    return run_query("""
        SELECT
            COUNT(DISTINCT c.customer_id)                                    AS total_customers,
            ROUND(SUM(p.amount)::numeric, 2)                                 AS total_revenue,
            COUNT(DISTINCT r.rental_id)                                      AS total_rentals,
            ROUND(AVG(p.amount)::numeric, 2)                                 AS avg_transaction,
            ROUND(SUM(p.amount)/COUNT(DISTINCT c.customer_id), 2)            AS avg_spend_per_customer
        FROM customer c
        JOIN rental  r ON c.customer_id = r.customer_id
        JOIN payment p ON r.rental_id   = p.rental_id
    """)

@st.cache_data(ttl=600)
def load_customer_summary():
    df = run_query("""
        SELECT
            cu.customer_id,
            cu.first_name || ' ' || cu.last_name                              AS customer_name,
            COUNT(DISTINCT r.rental_id)                                        AS rental_count,
            ROUND(SUM(p.amount)::numeric, 2)                                   AS total_revenue,
            ROUND(AVG(p.amount)::numeric, 2)                                   AS avg_payment,
            ROUND(AVG(EXTRACT(EPOCH FROM (r.return_date - r.rental_date))
                  / 86400.0)::numeric, 1)                                      AS avg_duration_days
        FROM customer cu
        JOIN rental  r ON cu.customer_id = r.customer_id
        JOIN payment p ON r.rental_id    = p.rental_id
        WHERE r.return_date IS NOT NULL
        GROUP BY cu.customer_id, cu.first_name, cu.last_name
    """)
    for col in ["total_revenue","avg_payment","avg_duration_days"]:
        df[col] = df[col].astype(float)
    return df

@st.cache_data(ttl=600)
def load_monthly_revenue():
    df = run_query("""
        SELECT
            DATE_TRUNC('month', payment_date) AS month,
            SUM(amount)                        AS revenue,
            COUNT(*)                           AS transactions,
            COUNT(DISTINCT customer_id)        AS active_customers
        FROM payment
        GROUP BY 1 ORDER BY 1
    """)
    df["month"]       = pd.to_datetime(df["month"])
    df["revenue"]     = df["revenue"].astype(float)
    df["month_label"] = df["month"].dt.strftime("%b %Y")
    return df

@st.cache_data(ttl=600)
def load_duration_dist():
    df = run_query("""
        SELECT ROUND(EXTRACT(EPOCH FROM (return_date - rental_date)) / 86400.0, 1) AS duration_days
        FROM rental WHERE return_date IS NOT NULL
    """)
    df["duration_days"] = df["duration_days"].astype(float)
    return df

@st.cache_data(ttl=600)
def load_genre():
    return run_query("""
        SELECT cat.name AS genre, COUNT(DISTINCT r.rental_id) AS rental_count
        FROM rental r
        JOIN inventory     i   ON r.inventory_id  = i.inventory_id
        JOIN film          f   ON i.film_id        = f.film_id
        JOIN film_category fc  ON f.film_id        = fc.film_id
        JOIN category      cat ON fc.category_id   = cat.category_id
        GROUP BY cat.name ORDER BY rental_count DESC
    """)

@st.cache_data(ttl=600)
def load_geography():
    return run_query("""
        SELECT co.country, COUNT(DISTINCT c.customer_id) AS customer_count
        FROM customer c
        JOIN address a  ON c.address_id  = a.address_id
        JOIN city    ci ON a.city_id     = ci.city_id
        JOIN country co ON ci.country_id = co.country_id
        GROUP BY co.country ORDER BY customer_count DESC LIMIT 15
    """)

@st.cache_data(ttl=600)
def load_rfm_segments():
    return run_query("""
        WITH rfm AS (
            SELECT
                c.customer_id,
                c.first_name || ' ' || c.last_name       AS customer_name,
                c.email,
                MAX(r.rental_date)::date                  AS last_rental_date,
                COUNT(DISTINCT r.rental_id)               AS frequency,
                ROUND(SUM(p.amount)::numeric, 2)          AS monetary,
                (SELECT MAX(rental_date)::date FROM rental)
                    - MAX(r.rental_date)::date            AS recency_days
            FROM customer c
            JOIN rental  r ON c.customer_id = r.customer_id
            JOIN payment p ON r.rental_id   = p.rental_id
            GROUP BY c.customer_id, customer_name, c.email
        )
        SELECT *,
            CASE
                WHEN recency_days <= 30  AND frequency >= 30 AND monetary >= 150 THEN 'Champions'
                WHEN recency_days <= 60  AND (frequency >= 20 OR monetary >= 100) THEN 'Loyal'
                WHEN recency_days BETWEEN 61 AND 120                              THEN 'At Risk'
                ELSE 'Lost'
            END AS segment
        FROM rfm ORDER BY monetary DESC
    """)

@st.cache_data(ttl=600)
def load_store():
    return run_query("""
        SELECT
            'Store ' || s.store_id           AS store_label,
            COUNT(DISTINCT r.customer_id)    AS unique_customers,
            COUNT(DISTINCT r.rental_id)      AS rental_count,
            ROUND(SUM(p.amount)::numeric, 2) AS revenue
        FROM store s
        JOIN inventory i ON s.store_id     = i.store_id
        JOIN rental    r ON i.inventory_id = r.inventory_id
        JOIN payment   p ON r.rental_id    = p.rental_id
        GROUP BY s.store_id ORDER BY s.store_id
    """)

# ──────────────────────────────────────────────────────────────
# LOAD DATA
# ──────────────────────────────────────────────────────────────
try:
    df_kpi     = load_kpi()
    df_cust    = load_customer_summary()
    df_month   = load_monthly_revenue()
    df_dur     = load_duration_dist()
    df_genre   = load_genre()
    df_geo     = load_geography()
    df_seg     = load_rfm_segments()
    df_store   = load_store()
except Exception as e:
    st.error("❌ Cannot connect to PostgreSQL. Make sure dvdrental is running.")
    st.exception(e)
    st.stop()

# ── Assign spending segment ke semua customer ──
_seg_labels = pd.qcut(
    df_cust["total_revenue"], q=4,
    labels=["Low Spender","Mid Spender","High Spender","Top Spender"],
    duplicates="drop"
)
df_cust["spend_segment"] = _seg_labels

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div class="sb-brand">
    <div class="sb-logo">
        <svg width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="52" height="52" rx="14" fill="#1E2D5A"/>
            <rect x="1" y="1" width="50" height="50" rx="13" stroke="rgba(212,96,122,0.3)" stroke-width="1"/>
            <!-- bar chart batang -->
            <rect x="10" y="30" width="6" height="12" rx="2" fill="#3A4F8A"/>
            <rect x="19" y="22" width="6" height="20" rx="2" fill="#5A72A8"/>
            <rect x="28" y="16" width="6" height="26" rx="2" fill="#7A90C0"/>
            <rect x="37" y="10" width="6" height="32" rx="2" fill="#D4607A"/>
            <!-- garis tren naik -->
            <polyline points="13,29 22,21 31,15 40,9" fill="none" stroke="#F0AEC0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- titik di ujung tren -->
            <circle cx="40" cy="9" r="2.5" fill="#F0AEC0"/>
            <!-- titik kecil lainnya -->
            <circle cx="13" cy="29" r="1.8" fill="rgba(240,174,192,0.6)"/>
            <circle cx="22" cy="21" r="1.8" fill="rgba(240,174,192,0.6)"/>
            <circle cx="31" cy="15" r="1.8" fill="rgba(240,174,192,0.6)"/>
        </svg>
    </div>
    <span class="sb-brand-name">Customer Analytics</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("**🏆 Top N Customers**")
    top_n = st.slider("", min_value=5, max_value=30, value=10, step=5, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**📅 Month Range**")
    months = df_month.sort_values("month")["month_label"].tolist()
    selected_months = st.select_slider("", options=months, value=(months[0], months[-1]), label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**👥 Filter Spending Segment**")
    seg_all    = ["Low Spender","Mid Spender","High Spender","Top Spender"]
    seg_select = [s for s in seg_all if st.checkbox(s, value=True, key=f"seg_{s}")]
    if not seg_select:
        seg_select = seg_all

# Apply filter
df_f = df_cust[df_cust["spend_segment"].isin(seg_select)].copy()

# Month filter untuk trend chart
month_start = selected_months[0]
month_end   = selected_months[1]
month_order = df_month.sort_values("month")["month_label"].tolist()
start_idx   = month_order.index(month_start)
end_idx     = month_order.index(month_end)
df_month_f  = df_month[df_month["month_label"].isin(month_order[start_idx:end_idx+1])]

# ──────────────────────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-logo-box">
        <div class="hero-logo-icon">
            <svg width="40" height="40" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="52" height="52" rx="14" fill="rgba(255,255,255,0.08)"/>
                <rect x="1" y="1" width="50" height="50" rx="13" stroke="rgba(240,174,192,0.25)" stroke-width="1"/>
                <rect x="10" y="30" width="6" height="12" rx="2" fill="rgba(255,255,255,0.2)"/>
                <rect x="19" y="22" width="6" height="20" rx="2" fill="rgba(255,255,255,0.3)"/>
                <rect x="28" y="16" width="6" height="26" rx="2" fill="rgba(255,255,255,0.45)"/>
                <rect x="37" y="10" width="6" height="32" rx="2" fill="#D4607A"/>
                <polyline points="13,29 22,21 31,15 40,9" fill="none" stroke="#F0AEC0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="40" cy="9" r="2.5" fill="#F0AEC0"/>
                <circle cx="13" cy="29" r="1.8" fill="rgba(240,174,192,0.5)"/>
                <circle cx="22" cy="21" r="1.8" fill="rgba(240,174,192,0.5)"/>
                <circle cx="31" cy="15" r="1.8" fill="rgba(240,174,192,0.5)"/>
            </svg>
        </div>
    </div>
    <div class="hero-text">
        <h1>Customer Analytics Dashboard</h1>
        <p>Revenue · Behavior · Loyalty · Segmentation — dvdrental</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# KPI ROW
# ──────────────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Key Metrics</div>', unsafe_allow_html=True)

kpi       = df_kpi.iloc[0]
top1      = df_f.nlargest(1, "total_revenue").iloc[0] if not df_f.empty else None
n_cust    = len(df_f)
total_rev = df_f["total_revenue"].sum()

kpis = [
    ("Total Customers",      f"{int(kpi['total_customers']):,}",              "active customers"),
    ("Total Revenue",        f"${float(kpi['total_revenue']):,.2f}",          "all transactions"),
    ("Total Rentals",        f"{int(kpi['total_rentals']):,}",                "all time"),
    ("Avg Revenue Per Rental Transaction",      f"${float(kpi['avg_transaction']):,.2f}",        "per payment"),
    ("Avg Spend Per Customer",   f"${float(kpi['avg_spend_per_customer']):,.2f}", "lifetime value"),
]

cols = st.columns(5)
for col, (label, val, sub) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-sub"><span class="kpi-dot"></span>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Behavior",
    "Loyalty & Segments",
    "Customer Detail",
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════
with tab1:

    # ── Monthly Revenue Trend ──
    st.markdown('<div class="sec-label">Revenue Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Monthly Revenue & Transactions</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Total payment collected per month — filtered by sidebar date range</div>', unsafe_allow_html=True)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_month_f["month_label"], y=df_month_f["revenue"],
        mode="lines+markers", name="Revenue",
        line=dict(color=NAVY, width=3, shape="spline"),
        marker=dict(size=9, color=PINK, line=dict(width=2.5, color="#fff")),
        fill="tozeroy", fillcolor="rgba(30,45,90,0.07)",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>"
    ))
    fig_line.add_trace(go.Bar(
        x=df_month_f["month_label"], y=df_month_f["transactions"],
        name="Transactions", yaxis="y2",
        marker_color="rgba(212,96,122,0.18)",
        hovertemplate="<b>%{x}</b><br>Transactions: %{y:,}<extra></extra>"
    ))
    fig_line = fig_base(fig_line, h=300, legend=True)
    fig_line.update_layout(
        yaxis=dict(title="Revenue ($)", tickprefix="$"),
        yaxis2=dict(title="Transactions", overlaying="y", side="right",
                    gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10, color=PINK)),
        legend=dict(orientation="h", yanchor="top", y=1.12, xanchor="right", x=1),
        bargap=0.35
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Top Customers + Geography ──
    st.markdown('<div class="sec-label">Customer Overview</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        top_n_share = (df_f.nlargest(top_n, "total_revenue")["total_revenue"].sum()
                       / df_f["total_revenue"].sum() * 100) if not df_f.empty else 0
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-title">Top {top_n} Customers by Spending</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-sub">Top {top_n} customers contribute <b style="color:#D4607A">{top_n_share:.0f}%</b> of filtered revenue</div>', unsafe_allow_html=True)

        top_c = df_f.nlargest(top_n, "total_revenue").sort_values("total_revenue", ascending=True)
        n     = len(top_c)
        bar_colors = [NAVY if i >= n-3 else "#7A90C0" for i in range(n)]
        if n > 0:
            bar_colors[-1] = PINK

        fig_bar = go.Figure(go.Bar(
            x=top_c["total_revenue"], y=top_c["customer_name"], orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=top_c["total_revenue"].apply(lambda v: f"${v:,.0f}"),
            textposition="outside", textfont=dict(size=9, color=SLATE),
            hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>"
        ))
        fig_bar = fig_base(fig_bar, h=420)
        fig_bar.update_layout(
            xaxis=dict(tickprefix="$", title="Total Revenue ($)"),
            yaxis=dict(title="", tickfont=dict(size=9))
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Customer by Country</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Top 15 countries by number of customers</div>', unsafe_allow_html=True)

        fig_geo = go.Figure(go.Bar(
            x=df_geo["customer_count"],
            y=df_geo["country"],
            orientation="h",
            marker=dict(
                color=df_geo["customer_count"],
                colorscale=[[0,"#EEF1FB"],[0.5,"#7A90C0"],[1.0,NAVY]],
                showscale=False, line=dict(width=0)
            ),
            text=df_geo["customer_count"], textposition="outside",
            textfont=dict(size=9),
            hovertemplate="<b>%{y}</b><br>Customers: %{x}<extra></extra>"
        ))
        fig_geo = fig_base(fig_geo, h=420)
        fig_geo.update_layout(
            xaxis=dict(title="Number of Customers"),
            yaxis=dict(title="", tickfont=dict(size=9), autorange="reversed")
        )
        st.plotly_chart(fig_geo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — BEHAVIOR
# ════════════════════════════════════════════════════════════════
with tab2:

    st.markdown('<div class="sec-label">Customer Rental Behavior</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    # ── Genre Preference ──
    with col_a:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Favorite Genres</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">What kind of films do customers love to rent?</div>', unsafe_allow_html=True)

        fig_genre = go.Figure(go.Bar(
            x=df_genre["rental_count"],
            y=df_genre["genre"],
            orientation="h",
            marker=dict(
                color=df_genre["rental_count"],
                colorscale=[[0,"#EEF1FB"],[0.5,NAVY],[1.0,PINK]],
                showscale=False, line=dict(width=0)
            ),
            text=df_genre["rental_count"], textposition="outside",
            textfont=dict(size=9),
            hovertemplate="<b>%{y}</b><br>Rentals: %{x:,}<extra></extra>"
        ))
        fig_genre = fig_base(fig_genre, h=400)
        fig_genre.update_layout(
            xaxis=dict(title="Total Rentals"),
            yaxis=dict(title="", autorange="reversed")
        )
        st.plotly_chart(fig_genre, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Scatter Frequency vs Spending ──
    with col_b:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">More Rentals = More Revenue</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Each dot = 1 customer — dashed line shows the trend</div>', unsafe_allow_html=True)

        q_colors = {
            "Low Spender":  "#C8D0E4",
            "Mid Spender":  "#7A90C0",
            "High Spender": NAVY,
            "Top Spender":  PINK
        }
        fig_sc = px.scatter(
            df_f, x="rental_count", y="total_revenue",
            color="spend_segment", color_discrete_map=q_colors,
            hover_name="customer_name",
            size="avg_duration_days", size_max=14,
            opacity=0.80, trendline="ols",
            labels={"rental_count":"Number of Rentals","total_revenue":"Total Revenue ($)","spend_segment":"Segment"}
        )
        fig_sc.update_traces(marker=dict(line=dict(width=0.8, color="#fff")), selector=dict(mode="markers"))
        fig_sc.update_traces(line=dict(color=PINK, width=2, dash="dash"), selector=dict(mode="lines"))
        fig_sc = fig_base(fig_sc, h=400, legend=True)
        fig_sc.update_yaxes(tickprefix="$", title="Total Revenue ($)")
        fig_sc.update_xaxes(title="Number of Rentals")
        fig_sc.update_layout(legend=dict(title="Spending Level", orientation="v", yanchor="bottom", y=0.02, xanchor="right", x=0.99))
        st.plotly_chart(fig_sc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Histogram Freq + Duration ──
    st.markdown('<div class="sec-label">Rental Distribution</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Rental Frequency Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Number of customers grouped by how many times they have rented</div>', unsafe_allow_html=True)

        fig_freq = go.Figure(go.Histogram(
            x=df_f["rental_count"], nbinsx=20,
            marker=dict(color=NAVY, opacity=0.85, line=dict(color="#fff", width=1.2)),
            hovertemplate="Rentals: %{x}<br>Customers: %{y}<extra></extra>"
        ))
        mean_freq = df_f["rental_count"].mean()
        fig_freq.add_vline(x=mean_freq, line_dash="dash", line_color=PINK, line_width=2,
                           annotation_text=f"Avg: {mean_freq:.1f}",
                           annotation_position="top right",
                           annotation_font=dict(size=10, color=PINK))
        fig_freq = fig_base(fig_freq, h=300)
        fig_freq.update_layout(
            xaxis=dict(title="Number of Rentals"),
            yaxis=dict(title="Number of Customers"),
            bargap=0.08
        )
        st.plotly_chart(fig_freq, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">How Long Do Customers Keep DVDs?</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Most rentals returned within a few days — supports steady cash flow</div>', unsafe_allow_html=True)

        dur_binned = (
            df_dur["duration_days"].clip(upper=12).round(0).astype(int)
            .value_counts().sort_index().reset_index()
        )
        dur_binned.columns = ["days","count"]

        fig_dur = go.Figure(go.Bar(
            x=dur_binned["days"], y=dur_binned["count"],
            marker=dict(
                color=dur_binned["count"],
                colorscale=[[0,"#C8D0E4"],[0.5,NAVY],[1.0,PINK]],
                showscale=False, line=dict(color="#fff", width=0.8)
            ),
            text=dur_binned["count"], textposition="outside",
            textfont=dict(size=9),
            hovertemplate="Duration: %{x} days<br>Rentals: %{y:,}<extra></extra>"
        ))
        mean_dur = df_dur["duration_days"].mean()
        fig_dur.add_vline(x=mean_dur, line_dash="dash", line_color=PINK, line_width=2,
                          annotation_text=f"Avg: {mean_dur:.1f}d",
                          annotation_position="top right",
                          annotation_font=dict(size=10, color=PINK))
        fig_dur = fig_base(fig_dur, h=300)
        fig_dur.update_layout(
            xaxis=dict(title="Days Until Return", dtick=1),
            yaxis=dict(title="Number of Rentals"),
            bargap=0.15
        )
        st.plotly_chart(fig_dur, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Cumulative Revenue Area ──
    st.markdown('<div class="sec-label">Revenue Growth</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Cumulative Revenue Growth</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">How customer spending has accumulated over time</div>', unsafe_allow_html=True)

    df_cum = df_month_f.copy()
    df_cum["cumulative_revenue"] = df_cum["revenue"].cumsum()
    fig_area = go.Figure(go.Scatter(
        x=df_cum["month_label"], y=df_cum["cumulative_revenue"],
        mode="lines", fill="tozeroy",
        line=dict(color=PINK, width=2.5),
        fillcolor="rgba(212,96,122,0.10)",
        hovertemplate="<b>%{x}</b><br>Cumulative: $%{y:,.0f}<extra></extra>"
    ))
    fig_area = fig_base(fig_area, h=260)
    fig_area.update_layout(yaxis=dict(tickprefix="$", title="Cumulative Revenue ($)"), xaxis=dict(title=""))
    st.plotly_chart(fig_area, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 3 — LOYALTY & SEGMENTS
# ════════════════════════════════════════════════════════════════
with tab3:

    # ── RFM Donut + Avg Spending Bar ──
    st.markdown('<div class="sec-label">RFM Segmentation</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.8rem;color:#8A97B5;margin:-0.5rem 0 1rem;">Based on Recency, Frequency, Monetary — who is the best customer?</p>', unsafe_allow_html=True)

    seg_summary = df_seg.groupby("segment").size().reset_index(name="count")
    seg_stats   = df_seg.groupby("segment").agg(
        avg_spent=("monetary","mean"),
        avg_freq=("frequency","mean"),
        count=("customer_id","count")
    ).reset_index()

    col_a, col_b = st.columns([1, 1.5])

    with col_a:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Segment Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Proporsi customer per segment RFM</div>', unsafe_allow_html=True)

        fig_donut = go.Figure(go.Pie(
            labels=seg_summary["segment"],
            values=seg_summary["count"],
            hole=0.55,
            marker=dict(
                colors=[SEG_COLORS.get(s,"#C8D0E4") for s in seg_summary["segment"]],
                line=dict(color="#fff", width=2.5)
            ),
            textinfo="label+percent", textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>Customers: %{value}<br>Share: %{percent}<extra></extra>"
        ))
        fig_donut.add_annotation(
            text=f"<b>{len(df_seg)}</b><br>customers",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=NAVY)
        )
        fig_donut = fig_base(fig_donut, h=320, legend=True)
        fig_donut.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5))
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Avg Spending per Segment</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Champions and loyal customers make the biggest contribution</div>', unsafe_allow_html=True)

        fig_seg_bar = go.Figure(go.Bar(
            x=seg_stats["segment"], y=seg_stats["avg_spent"],
            marker=dict(color=[SEG_COLORS.get(s,"#C8D0E4") for s in seg_stats["segment"]],
                        line=dict(color="#fff", width=1)),
            text=seg_stats["avg_spent"].apply(lambda v: f"${v:,.2f}"),
            textposition="outside", textfont=dict(size=10, color=SLATE),
            hovertemplate="<b>%{x}</b><br>Avg Spending: $%{y:,.2f}<extra></extra>"
        ))
        fig_seg_bar = fig_base(fig_seg_bar, h=320)
        fig_seg_bar.update_layout(
            yaxis=dict(tickprefix="$", title="Avg Spending ($)"),
            xaxis=dict(title="Customer Segment"),
            bargap=0.35
        )
        st.plotly_chart(fig_seg_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Segment KPI badges ──
    kc1, kc2, kc3 = st.columns(3)
    for col, seg, icon in zip([kc1, kc2, kc3],
                               ["Champions", "Loyal", "Lost"],
                               ["🏆", "💙", "🚀"]):
        cnt = seg_summary[seg_summary["segment"] == seg]["count"].values
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-label">{icon} {seg.upper()}</div>
                <div class="kpi-val">{cnt[0] if len(cnt) else 0}</div>
                <div class="kpi-sub"><span class="kpi-dot"></span>customers</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Spending Segment Donut (qcut) + Revenue Bar ──
    st.markdown('<div class="sec-label">Spending Tier Analysis</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns([1, 1.4])

    df_cust_full = load_customer_summary()
    _seg_full    = pd.qcut(df_cust_full["total_revenue"], q=4,
                           labels=["Low Spender","Mid Spender","High Spender","Top Spender"],
                           duplicates="drop")
    df_cust_full["segment"] = _seg_full
    seg_counts  = df_cust_full["segment"].value_counts().reindex(["Low Spender","Mid Spender","High Spender","Top Spender"]).fillna(0)
    seg_rev     = df_cust_full.groupby("segment", observed=False)["total_revenue"].sum().reindex(["Low Spender","Mid Spender","High Spender","Top Spender"]).fillna(0)
    tier_colors = ["#C8D0E4","#7A90C0",NAVY,PINK]

    with col_c:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Customer Count per Spending Tier</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Customer Distribution based on Spending Tiers</div>', unsafe_allow_html=True)

        fig_tier = go.Figure(go.Pie(
            labels=seg_counts.index.tolist(), values=seg_counts.values.tolist(),
            hole=0.55,
            marker=dict(colors=tier_colors, line=dict(color="#fff", width=2.5)),
            textinfo="label+percent", textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>Customers: %{value}<br>Share: %{percent}<extra></extra>"
        ))
        fig_tier.add_annotation(
            text=f"<b>{int(seg_counts.sum())}</b><br>customers",
            x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=NAVY)
        )
        fig_tier = fig_base(fig_tier, h=300, legend=True)
        fig_tier.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5))
        st.plotly_chart(fig_tier, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Revenue Contribution by Spending Tier</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Which tier actually drives the most revenue?</div>', unsafe_allow_html=True)

        seg_rev_pct = (seg_rev / seg_rev.sum() * 100).round(1)
        fig_rev_seg = go.Figure(go.Bar(
            x=seg_rev.index.tolist(), y=seg_rev.values.tolist(),
            marker=dict(color=tier_colors, line=dict(color="#fff", width=1)),
            text=[f"${v:,.0f}\n({p:.1f}%)" for v,p in zip(seg_rev.values, seg_rev_pct.values)],
            textposition="outside", textfont=dict(size=9, color=SLATE),
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>"
        ))
        fig_rev_seg = fig_base(fig_rev_seg, h=300)
        fig_rev_seg.update_layout(
            yaxis=dict(tickprefix="$", title="Total Revenue ($)"),
            xaxis=dict(title="Spending Tier"),
            bargap=0.35
        )
        st.plotly_chart(fig_rev_seg, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── At-Risk Customers ──
    st.markdown('<div class="sec-label">⚠️ At-Risk Customers</div>', unsafe_allow_html=True)
    at_risk = df_seg[df_seg["recency_days"] >= 90].copy()
    if at_risk.empty:
        st.success("✅ No at-risk customers found!")
    else:
        st.warning(f"⚠️ {len(at_risk)} customers haven't rented in 90+ days.")
        st.dataframe(
            at_risk[["customer_name","email","last_rental_date","frequency","monetary","recency_days"]]
            .rename(columns={
                "customer_name":    "Customer",
                "email":            "Email",
                "last_rental_date": "Last Rental",
                "frequency":        "Total Rentals",
                "monetary":         "Total Spent ($)",
                "recency_days":     "Days Inactive"
            }),
            use_container_width=True, hide_index=True
        )

    # ── Key Insights ──
    st.markdown('<div class="sec-label">Key Insights</div>', unsafe_allow_html=True)
    top20_pct = (df_f.nlargest(max(1,int(len(df_f)*0.2)), "total_revenue")["total_revenue"].sum()
                 / df_f["total_revenue"].sum() * 100) if not df_f.empty else 0
    corr      = df_f[["rental_count","total_revenue"]].corr().iloc[0,1] if len(df_f) > 1 else 0
    modal_dur = int(df_dur["duration_days"].round(0).mode()[0])
    avg_dur_v = df_dur["duration_days"].mean()

    st.markdown(f"""
    <div class="insight-row">
        <div class="insight-card">
            <h4>Revenue Concentration</h4>
            <span class="insight-num">{top20_pct:.0f}%</span>
            <p>of total revenue comes from the top 20% of customers — a small group of high-value customers drives most of the business.</p>
        </div>
        <div class="insight-card">
            <h4>Frequency Drives Revenue</h4>
            <span class="insight-num">r = {corr:.2f}</span>
            <p>correlation between rental frequency and revenue. The more a customer rents, the more they spend — confirmed by the scatter trendline.</p>
        </div>
        <div class="insight-card">
            <h4>Return Behavior</h4>
            <span class="insight-num">{modal_dur} days</span>
            <p>is the most common rental duration. Average is {avg_dur_v:.1f} days. Fast returns support steady transaction flow and consistent revenue.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 4 — CUSTOMER DETAIL
# ════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-label">Deep Dive — Individual Customer</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.8rem;color:#8A97B5;margin:-0.5rem 0 1rem;">Search a customer and explore their full rental history & preferences.</p>', unsafe_allow_html=True)

    search_name = st.text_input("🔍 Search Customer Name", placeholder="e.g. Eleanor, Karl, Marion...")

    if not search_name:
        st.info("👆 Type a customer name above to see their profile.")
    else:
        try:
            cust_list = run_query(f"""
                SELECT c.customer_id, c.first_name||' '||c.last_name AS customer_name,
                       c.email, co.country, c.active
                FROM customer c
                JOIN address a  ON c.address_id  = a.address_id
                JOIN city    ci ON a.city_id      = ci.city_id
                JOIN country co ON ci.country_id  = co.country_id
                WHERE LOWER(c.first_name||' '||c.last_name) LIKE LOWER('%{search_name}%')
                ORDER BY customer_name LIMIT 20
            """)
        except Exception as e:
            st.error(f"Search error: {e}")
            cust_list = pd.DataFrame()

        if cust_list.empty:
            st.warning(f"No customer found with name containing '{search_name}'.")
        else:
            sel_name = st.selectbox("Select Customer", cust_list["customer_name"].tolist())
            row      = cust_list[cust_list["customer_name"]==sel_name].iloc[0]
            cust_id  = int(row["customer_id"])

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1E2D5A,#2E4080);border-radius:14px;
                        padding:1.3rem 1.6rem;margin:1rem 0;display:flex;gap:1rem;align-items:center;">
                <div style="font-size:2.5rem;">👤</div>
                <div>
                    <div style="font-size:1.2rem;font-weight:800;color:#fff;">{row['customer_name']}</div>
                    <div style="font-size:0.8rem;color:#A8B8D8;margin-top:4px;">
                        📧 {row['email']} &nbsp;|&nbsp; 🌍 {row['country']} &nbsp;|&nbsp;
                        {'🟢 Active' if row['active'] else '🔴 Inactive'}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            try:
                ck = run_query(f"""
                    SELECT COUNT(DISTINCT r.rental_id)         AS total_rentals,
                           ROUND(SUM(p.amount)::numeric,2)     AS total_spent,
                           ROUND(AVG(p.amount)::numeric,2)     AS avg_transaction,
                           MAX(r.rental_date)::date            AS last_rental,
                           MIN(r.rental_date)::date            AS first_rental
                    FROM rental r JOIN payment p ON r.rental_id=p.rental_id
                    WHERE r.customer_id={cust_id}
                """).iloc[0]

                kc = st.columns(5)
                detail_kpis = [
                    ("Total Rentals",    f"{int(ck['total_rentals']):,}",         "rentals"),
                    ("Total Spent",      f"${float(ck['total_spent']):,.2f}",     "lifetime"),
                    ("Avg Transaction",  f"${float(ck['avg_transaction']):,.2f}", "per payment"),
                    ("First Rental",     str(ck["first_rental"]),                 "joined"),
                    ("Last Rental",      str(ck["last_rental"]),                  "most recent"),
                ]
                for col, (label, val, sub) in zip(kc, detail_kpis):
                    with col:
                        st.markdown(f"""
                        <div class="kpi">
                            <div class="kpi-label">{label}</div>
                            <div class="kpi-val">{val}</div>
                            <div class="kpi-sub"><span class="kpi-dot"></span>{sub}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Customer KPI error: {e}")

            col_x, col_y = st.columns(2)

            with col_x:
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">Rental Activity Over Time</div>', unsafe_allow_html=True)
                st.markdown('<div class="chart-sub">How active has this customer been?</div>', unsafe_allow_html=True)
                try:
                    tl = run_query(f"""
                        SELECT TO_CHAR(r.rental_date,'YYYY-MM') AS rental_month,
                               COUNT(DISTINCT r.rental_id)      AS rental_count
                        FROM rental r WHERE r.customer_id={cust_id}
                        GROUP BY rental_month ORDER BY rental_month
                    """)
                    fig_tl = go.Figure(go.Scatter(
                        x=tl["rental_month"], y=tl["rental_count"],
                        mode="lines+markers",
                        line=dict(color=NAVY, width=2.5),
                        marker=dict(size=8, color=PINK, line=dict(width=2,color="#fff")),
                        fill="tozeroy", fillcolor="rgba(30,45,90,0.07)",
                        hovertemplate="<b>%{x}</b><br>Rentals: %{y}<extra></extra>"
                    ))
                    fig_tl = fig_base(fig_tl, h=260)
                    fig_tl.update_layout(xaxis=dict(title="Month"), yaxis=dict(title="Rentals"))
                    st.plotly_chart(fig_tl, use_container_width=True)
                except Exception as e:
                    st.error(f"Timeline error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_y:
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">Favorite Genres</div>', unsafe_allow_html=True)
                st.markdown('<div class="chart-sub">What does this customer love to watch?</div>', unsafe_allow_html=True)
                try:
                    g = run_query(f"""
                        SELECT cat.name AS genre, COUNT(DISTINCT r.rental_id) AS rental_count
                        FROM rental r
                        JOIN inventory     i   ON r.inventory_id=i.inventory_id
                        JOIN film          f   ON i.film_id=f.film_id
                        JOIN film_category fc  ON f.film_id=fc.film_id
                        JOIN category      cat ON fc.category_id=cat.category_id
                        WHERE r.customer_id={cust_id}
                        GROUP BY cat.name ORDER BY rental_count DESC
                    """)
                    fig_g = go.Figure(go.Bar(
                        x=g["rental_count"], y=g["genre"], orientation="h",
                        marker=dict(
                            color=g["rental_count"],
                            colorscale=[[0,"#EEF1FB"],[0.5,NAVY],[1.0,PINK]],
                            showscale=False, line=dict(width=0)
                        ),
                        text=g["rental_count"], textposition="outside",
                        textfont=dict(size=9),
                        hovertemplate="<b>%{y}</b><br>Rentals: %{x}<extra></extra>"
                    ))
                    fig_g = fig_base(fig_g, h=260)
                    fig_g.update_layout(
                        xaxis=dict(title="Rentals"),
                        yaxis=dict(title="", autorange="reversed")
                    )
                    st.plotly_chart(fig_g, use_container_width=True)
                except Exception as e:
                    st.error(f"Genre error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="sec-label">Rental History</div>', unsafe_allow_html=True)
            with st.expander("View Full Rental History", expanded=False):
                try:
                    hist = run_query(f"""
                        SELECT r.rental_id, r.rental_date::date AS rental_date,
                               r.return_date::date AS return_date,
                               f.title AS film_title, cat.name AS genre, p.amount AS paid
                        FROM rental r
                        JOIN inventory     i   ON r.inventory_id=i.inventory_id
                        JOIN film          f   ON i.film_id=f.film_id
                        JOIN film_category fc  ON f.film_id=fc.film_id
                        JOIN category      cat ON fc.category_id=cat.category_id
                        JOIN payment       p   ON r.rental_id=p.rental_id
                        WHERE r.customer_id={cust_id}
                        ORDER BY r.rental_date DESC
                    """)
                    st.dataframe(
                        hist.rename(columns={"rental_id":"ID","rental_date":"Rental Date",
                                             "return_date":"Return Date","film_title":"Film",
                                             "genre":"Genre","paid":"Paid ($)"}),
                        use_container_width=True, hide_index=True, height=360
                    )
                except Exception as e:
                    st.error(f"History error: {e}")

# ──────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;font-size:0.70rem;color:#B0BAD0;padding-bottom:1rem;">
    Customer Analytics &nbsp;·&nbsp;
""", unsafe_allow_html=True)
