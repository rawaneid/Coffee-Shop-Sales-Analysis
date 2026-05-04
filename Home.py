import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Coffee Shop Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=Playfair+Display:wght@600&display=swap');

/* Global */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1A0F07;
}
[data-testid="stSidebar"] * { color: #E8C9A0 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important;
    padding: 6px 0 !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* Main background */
.main { background-color: #FDF8F1; }

/* KPI metric cards */
[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #EDE4D4;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    border-top: 3px solid #C8743D;
}
[data-testid="metric-container"] label {
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #8B7355 !important;
    font-weight: 500 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
    color: #1A0F07 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Section headers */
h1 { font-family: 'Playfair Display', serif !important; color: #1A0F07 !important; }
h2 { font-family: 'Playfair Display', serif !important; color: #1A0F07 !important; }
h3 { font-family: 'Playfair Display', serif !important; color: #1A0F07 !important; }

/* Divider */
hr { border-color: #EDE4D4 !important; }

/* Insight cards */
.insight-card {
    background: #FFFFFF;
    border: 1px solid #EDE4D4;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 14px;
    border-left: 4px solid #C8743D;
}
.insight-card h4 { margin: 0 0 5px 0; font-size: 15px; color: #1A0F07; font-weight: 500; }
.insight-card p  { margin: 0; font-size: 13px; color: #6B5D52; line-height: 1.6; }

.tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 20px;
    margin-bottom: 6px;
}
.tag-growth  { background: #EEF8EE; color: #1E6B1E; }
.tag-action  { background: #FEF3E8; color: #9B5000; }
.tag-warning { background: #FEF0EE; color: #9B2A1E; }
.tag-info    { background: #EEF2FE; color: #2A44A0; }

/* Conclusion box */
.conclusion-box {
    background: #1A0F07;
    border-radius: 12px;
    padding: 1.75rem 2rem;
    margin-top: 1.5rem;
}
.conclusion-box h3 { color: #E8C9A0 !important; margin-bottom: 10px; font-size: 18px; }
.conclusion-box p  { color: rgba(232,201,160,0.78); font-size: 14px; line-height: 1.8; margin: 0 0 10px 0; }

/* Highlight banner */
.highlight-banner {
    background: linear-gradient(135deg, #3B1E0A, #6B3A1F);
    border-radius: 12px;
    padding: 1.25rem 1.75rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.highlight-stat { text-align: center; }
.highlight-stat .label { font-size: 11px; color: rgba(232,201,160,0.6); text-transform: uppercase; letter-spacing: 0.06em; }
.highlight-stat .value { font-family: 'Playfair Display', serif; font-size: 20px; color: #E8C9A0; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Load & cache data ──────────────────────────────────────────────────────────
DAY_ORDER   = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
MONTH_ORDER = ["January","February","March","April","May","June"]

@st.cache_data
def load_data():
    df = pd.read_csv("Coffee_shop_sales_cleaned.csv")
    # Apply Categorical ordering so groupby sorts correctly
    df["Day Name"]   = pd.Categorical(df["Day Name"],   categories=DAY_ORDER,   ordered=True)
    df["Month Name"] = pd.Categorical(df["Month Name"], categories=MONTH_ORDER, ordered=True)
    return df

df = load_data()

# ── Shared plotly theme ────────────────────────────────────────────────────────
COLORS     = ["#C8743D","#6B3A1F","#E8C9A0","#8B7355","#3B1E0A","#D4A574","#F0DEC0"]
ACCENT     = "#C8743D"
BG         = "rgba(0,0,0,0)"
FONT_COLOR = "#1A0F07"
GRID_COLOR = "#EDE4D4"

def base_layout(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="DM Sans", color=FONT_COLOR, size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont_size=11)
    fig.update_yaxes(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont_size=11)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ☕ Coffee Shop")
    st.markdown("**Sales Analytics Dashboard**")
    st.markdown("*Jan – Jun 2023 · 3 Locations*")
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠  Overview", "📅  Time Trends", "☕  Products", "📋  About Dataset"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Dataset brief**")
    st.markdown("- **149,116** transactions")
    st.markdown("- **3** store locations")
    st.markdown("- **9** product categories")
    st.markdown("- **$698,812** total revenue")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Overview":
    st.title("Sales Overview")
    st.markdown("A snapshot of overall performance across all three store locations · Jan–Jun 2023")
    st.divider()

    # ── KPI row ──
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Revenue",           "$698,812",  "Jan → Jun +103.8%")
    k2.metric("Total Transactions",      "149,116",   "Steady monthly growth")
    k3.metric("Avg Bill / Transaction",  "$4.69",     "Consistent across stores")
    k4.metric("Avg Items / Transaction", "1.44",      "Median = 1 item")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Highlight banner ──
    st.markdown("""
    <div class="highlight-banner">
        <div class="highlight-stat"><div class="label">Best Month</div><div class="value">June</div></div>
        <div class="highlight-stat"><div class="label">June Revenue</div><div class="value">$166,486</div></div>
        <div class="highlight-stat"><div class="label">Top Store</div><div class="value">Hell's Kitchen</div></div>
        <div class="highlight-stat"><div class="label">Peak Hour</div><div class="value">10 AM</div></div>
        <div class="highlight-stat"><div class="label">#1 Product Type</div><div class="value">Barista Espresso</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Monthly revenue + store donut ──
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Monthly Revenue")
        df_month = (df.groupby(["Month", "Month Name"], observed=True)["Total_Bill"]
                      .sum().reset_index().sort_values("Month"))
        fig = px.bar(
            df_month, x="Month Name", y="Total_Bill",
            color_discrete_sequence=[ACCENT],
            text=df_month["Total_Bill"].apply(lambda v: f"${v/1000:.0f}K"),
            labels={"Month Name": "", "Total_Bill": "Revenue ($)"},
        )
        base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenue by Store")
        df_store = df.groupby("store_location")["Total_Bill"].sum().reset_index()
        fig = px.pie(
            df_store, names="store_location", values="Total_Bill",
            hole=0.55, color_discrete_sequence=COLORS,
            labels={"store_location": "Store", "Total_Bill": "Revenue ($)"},
        )
        fig.update_traces(textposition="outside", textinfo="label+percent")
        fig.update_layout(showlegend=False)
        base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Transactions + weekday vs weekend ──
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Monthly Transactions")
        df_txn = (df.groupby(["Month", "Month Name"], observed=True)["transaction_id"]
                    .count().reset_index().sort_values("Month"))
        df_txn.columns = ["Month", "Month Name", "Transactions"]
        fig = px.line(
            df_txn, x="Month Name", y="Transactions",
            markers=True, color_discrete_sequence=[ACCENT],
            labels={"Month Name": "", "Transactions": "Number of Transactions"},
        )
        fig.update_traces(line_width=2.5, marker_size=8)
        base_layout(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Weekday vs Weekend Revenue")
        df_dt = df.groupby("Day_Type")["Total_Bill"].sum().reset_index()
        fig = px.bar(
            df_dt, x="Day_Type", y="Total_Bill",
            color="Day_Type", color_discrete_sequence=[ACCENT, "#E8C9A0"],
            text=df_dt["Total_Bill"].apply(lambda v: f"${v/1000:.0f}K"),
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue ($)")
        base_layout(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — TIME TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅  Time Trends":
    st.title("Time Trends")
    st.markdown("When do customers visit and when does revenue peak? Explore by hour, day, and time of day.")
    st.divider()

    # ── Hourly revenue ──
    st.subheader("Revenue by Hour of Day")
    st.caption("The 8–10 AM morning rush generates 37% of total daily revenue")
    df_hour = df.groupby("Hour")["Total_Bill"].sum().reset_index()
    fig = px.area(
        df_hour, x="Hour", y="Total_Bill",
        color_discrete_sequence=[ACCENT],
        markers=True,
        labels={"Hour": "Hour of Day", "Total_Bill": "Revenue ($)"},
    )
    fig.update_traces(
        line_width=2.5,
        marker=dict(size=7),
        fillcolor="rgba(200,116,61,0.12)",
    )
    fig.update_layout(
        xaxis=dict(
            tickmode="linear", dtick=1,
            ticktext=[f"{h}:00" for h in range(6, 21)],
            tickvals=list(range(6, 21)),
        ),
        yaxis_title="Revenue ($)",
        xaxis_title="Hour of Day",
    )
    fig.add_vrect(
        x0=7.5, x1=10.5,
        fillcolor="rgba(200,116,61,0.08)",
        line_width=0,
        annotation_text="Peak window",
        annotation_position="top left",
    )
    base_layout(fig, height=360)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Day of Week")
        st.caption("Monday leads; Saturday is the slowest day")
        df_day = (df.groupby("Day Name", observed=True)["Total_Bill"]
                    .sum().reset_index().sort_values("Day Name"))
        fig = px.bar(
            df_day, x="Day Name", y="Total_Bill",
            color_discrete_sequence=[ACCENT],
            text=df_day["Total_Bill"].apply(lambda v: f"${v/1000:.0f}K"),
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(xaxis_title="", yaxis_title="Revenue ($)")
        base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenue by Time of Day")
        st.caption("Morning dominates; evenings are nearly inactive")
        df_tod = df.groupby("Day_time")["Total_Bill"].sum().reset_index()
        order_map = {"Morning": 0, "Afternoon": 1, "Evening": 2, "Night": 3}
        df_tod["sort"] = df_tod["Day_time"].map(order_map)
        df_tod = df_tod.sort_values("sort")
        fig = px.pie(
            df_tod, names="Day_time", values="Total_Bill",
            hole=0.5, color_discrete_sequence=COLORS,
        )
        fig.update_traces(textposition="outside", textinfo="label+percent")
        fig.update_layout(showlegend=False)
        base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Heatmap ──
    st.subheader("Revenue Heatmap — Day × Hour")
    st.caption("Darkest cells = highest revenue. The top-left block (Mon–Fri, 8–10 AM) is where the money is made.")
    pivot = (df.groupby(["Day Name", "Hour"], observed=True)["Total_Bill"]
               .sum().reset_index()
               .pivot(index="Day Name", columns="Hour", values="Total_Bill"))
    pivot = pivot.reindex(DAY_ORDER)
    fig = px.imshow(
        pivot,
        color_continuous_scale=["#FDF8F1","#E8C9A0","#C8743D","#6B3A1F","#1A0F07"],
        aspect="auto",
        labels=dict(x="Hour of Day", y="", color="Revenue ($)"),
    )
    fig.update_xaxes(tickmode="linear", dtick=1)
    base_layout(fig, height=300)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PRODUCTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "☕  Products":
    st.title("Product Analysis")
    st.markdown("Which products and categories drive the most revenue and transactions?")
    st.divider()

    tab1, tab2 = st.tabs(['Product Category', 'Order Size'])

    with tab1:
        st.subheader("Top 10 Product Types by Revenue")
        st.caption("Barista Espresso is the single highest-revenue product type")
        selected_categories = st.multiselect(
            "Filter by Product Category",df["product_category"].unique()
        )

        df_filtered = df[df["product_category"].isin(selected_categories)] if selected_categories else df

        df_pt = (df_filtered.groupby("product_type")["Total_Bill"]
                    .sum().reset_index()
                    .sort_values("Total_Bill", ascending=False).head(10))
        fig = px.bar(
            df_pt, x="Total_Bill", y="product_type",
            orientation="h", color_discrete_sequence=[ACCENT],
            text=df_pt["Total_Bill"].apply(lambda v: f"${v/1000:.0f}K"),
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(yaxis=dict(autorange="reversed"),
                            xaxis_title="Revenue ($)", yaxis_title="")
        base_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Category Mix")
        st.caption("By number of transactions")
        df_cat = df["product_category"].value_counts().reset_index()
        df_cat.columns = ["Category", "Count"]
        fig = px.pie(
            df_cat, names="Category", values="Count",
            hole=0.55, color_discrete_sequence=COLORS,
        )
        fig.update_traces(textposition="outside", textinfo="label+percent")
        st.plotly_chart(fig)

        # ── Product category by store ──
        st.subheader("Revenue by Category per Store")
        st.caption("All stores share a similar product mix — the model is consistent and scalable")

        f1, f2 = st.columns(2)
        selected_stores = f1.multiselect("Store", sorted(df["store_location"].unique()), default=sorted(df["store_location"].unique()))
        selected_cats   = f2.multiselect("Category", sorted(df["product_category"].unique()), default=sorted(df["product_category"].unique()))

        df_cs = df[df["store_location"].isin(selected_stores) & df["product_category"].isin(selected_cats)]
        df_cs = df_cs.groupby(["store_location", "product_category"])["Total_Bill"].sum().reset_index()

        fig = px.bar(
            df_cs, x="store_location", y="Total_Bill",
            color="product_category", barmode="group",
            color_discrete_sequence=COLORS,
            labels={"store_location": "Store", "Total_Bill": "Revenue ($)", "product_category": "Category"},
        )
        fig.update_layout(xaxis_title="", legend_title="Category")
        base_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Order Size Distribution")
            st.caption("Regular and Large sizes dominate; Small is rare")
            df_size = df["Size"].value_counts().reset_index()
            df_size.columns = ["Size", "Count"]
            size_order = ["Small", "Regular", "Large", "Not Defined"]
            df_size["Size"] = pd.Categorical(df_size["Size"], categories=size_order, ordered=True)
            df_size = df_size.sort_values("Size")
            fig = px.bar(
                df_size, x="Size", y="Count",
                color_discrete_sequence=[ACCENT],
                text="Count",
            )
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(xaxis_title="", yaxis_title="Number of Orders")
            base_layout(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.subheader("Avg Bill by Size")
            st.caption("Large orders earn 59% more than Small — upselling works")
            size_order = ["Small", "Regular", "Large", "Not Defined"]
            size_rev = df.groupby("Size")["Total_Bill"].mean().reset_index()
            size_rev.columns = ["Size", "Avg Bill"]
            size_rev["Size"] = pd.Categorical(size_rev["Size"], categories=size_order, ordered=True)
            size_rev = size_rev.sort_values("Size")
            size_rev["Label"] = size_rev["Avg Bill"].apply(lambda v: f"${v:.2f}")
            fig = px.bar(
                size_rev, x="Size", y="Avg Bill",
                color_discrete_sequence=["#6B3A1F"],
                text="Label",
            )
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(xaxis_title="", yaxis_title="Avg Bill ($)")
            base_layout(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — ABOUT DATASET
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋  About Dataset":
    st.title("About the Dataset")
    st.divider()

    st.subheader("Key Columns")
    cols_info = {
        "Column":      ["Total_Bill", "store_location", "product_category",
                        "product_type", "Hour", "Size", "Day Name", "Month Name"],
        "Description": [
            "Transaction total (qty × unit price)",
            "Astoria · Hell's Kitchen · Lower Manhattan",
            "Coffee, Tea, Bakery, Chocolate, etc.",
            "Specific product sub-type (e.g. Barista Espresso)",
            "Hour of transaction (6 AM – 8 PM)",
            "Small · Regular · Large · Not Defined",
            "Day of the week the transaction occurred",
            "Month name extracted from transaction date",
        ],
    }
    st.dataframe(pd.DataFrame(cols_info), hide_index=True, use_container_width=True)

    st.subheader("Dataset Preview")
    st.caption("First 100 rows of the cleaned dataset")
    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True,
    )