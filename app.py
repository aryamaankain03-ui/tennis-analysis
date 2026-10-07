import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Tennis Intelligence Studio",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# NAVIGATION CONSTANTS
NAV_OVERVIEW = "🏠 Executive Overview"
NAV_COMPETITIONS = "🏆 Competition Analytics"
NAV_VENUES = "🏟️ Venues & Logistics"
NAV_RANKINGS = "🎾 Player Rankings"

# Color Palette Definitions (Professional Theme)
PRIMARY_COLOR = "#0F172A"
ACCENT_COLOR = "#2563EB"
BG_COLOR = "#F8FAFC"
CARD_BG = "#FFFFFF"
TEXT_COLOR = "#1E293B"
MUTED_TEXT = "#64748B"
BORDER_COLOR = "#E2E8F0"

# ============================================================
# ADVANCED CUSTOM CSS
# ============================================================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Global Background */
    .stApp {{
        background-color: {BG_COLOR};
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {PRIMARY_COLOR};
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}

    section[data-testid="stSidebar"] * {{
        color: #F1F5F9 !important;
    }}

    /* Title Styling */
    .main-header {{
        padding: 10px 0px 25px 0px;
    }}
    .main-title {{
        font-size: 32px;
        font-weight: 800;
        color: {TEXT_COLOR};
        letter-spacing: -0.5px;
    }}
    .main-subtitle {{
        font-size: 15px;
        color: {MUTED_TEXT};
        margin-top: 4px;
    }}

    /* Custom Metric / KPI Cards */
    .kpi-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.08);
    }}
    .kpi-title {{
        font-size: 13px;
        font-weight: 600;
        color: {MUTED_TEXT};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        font-size: 28px;
        font-weight: 700;
        color: {TEXT_COLOR};
    }}

    /* Tab Customization */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        border-bottom: 1px solid {BORDER_COLOR};
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 45px;
        white-space: pre-wrap;
        border-radius: 8px 8px 0px 0px;
        font-weight: 600;
        font-size: 14px;
        color: {MUTED_TEXT};
    }}
    .stTabs [aria-selected="true"] {{
        color: {ACCENT_COLOR} !important;
        border-bottom: 2px solid {ACCENT_COLOR} !important;
    }}

    /* Section Headers */
    .section-header {{
        font-size: 18px;
        font-weight: 700;
        color: {TEXT_COLOR};
        margin: 20px 0 12px 0;
    }}

    /* Status Pill */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
    }}
    .status-success {{
        background-color: #DCFCE7;
        color: #166534;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DATA SOURCE INITIALIZATION
# ============================================================
@st.cache_data
def load_data():
    """Load mock dataset replacing MySQL database backend."""
    categories_df = pd.DataFrame([
        {"category_id": 1, "category_name": "ATP Tour"},
        {"category_id": 2, "category_name": "WTA Tour"},
        {"category_id": 3, "category_name": "ITF Men"},
        {"category_id": 4, "category_name": "ITF Women"},
        {"category_id": 5, "category_name": "Challenger Tour"},
        {"category_id": 6, "category_name": "Grand Slam"},
        {"category_id": 7, "category_name": "Davis Cup"},
        {"category_id": 8, "category_name": "BJK Cup"},
        {"category_id": 9, "category_name": "Olympics"},
        {"category_id": 10, "category_name": "Exhibition"}
    ])

    competitions_df = pd.DataFrame([
        {"competition_id": 101, "competition_name": "Australian Open Men Singles", "type": "singles", "gender": "men", "category_id": 6, "parent_id": None},
        {"competition_id": 102, "competition_name": "Australian Open Men Doubles", "type": "doubles", "gender": "men", "category_id": 6, "parent_id": 101},
        {"competition_id": 103, "competition_name": "Roland Garros Women Singles", "type": "singles", "gender": "women", "category_id": 6, "parent_id": None},
        {"competition_id": 104, "competition_name": "Roland Garros Women Doubles", "type": "doubles", "gender": "women", "category_id": 6, "parent_id": 103},
        {"competition_id": 105, "competition_name": "Wimbledon Men Singles", "type": "singles", "gender": "men", "category_id": 6, "parent_id": None},
        {"competition_id": 106, "competition_name": "Wimbledon Men Doubles", "type": "doubles", "gender": "men", "category_id": 6, "parent_id": 105},
        {"competition_id": 107, "competition_name": "US Open Women Singles", "type": "singles", "gender": "women", "category_id": 6, "parent_id": None},
        {"competition_id": 108, "competition_name": "Indian Wells Masters", "type": "singles", "gender": "men", "category_id": 1, "parent_id": None},
        {"competition_id": 109, "competition_name": "Miami Open Doubles", "type": "doubles", "gender": "mixed", "category_id": 1, "parent_id": 108},
        {"competition_id": 110, "competition_name": "ITF Men Futures Chile", "type": "singles", "gender": "men", "category_id": 3, "parent_id": None},
        {"competition_id": 111, "competition_name": "ITF Men Doubles Santiago", "type": "doubles", "gender": "men", "category_id": 3, "parent_id": 110},
        {"competition_id": 112, "competition_name": "ITF Women W25 Zagreb", "type": "singles", "gender": "women", "category_id": 4, "parent_id": None},
        {"competition_id": 113, "competition_name": "Rome Masters Doubles", "type": "doubles", "gender": "men", "category_id": 1, "parent_id": None},
        {"competition_id": 114, "competition_name": "Madrid Open Women", "type": "singles", "gender": "women", "category_id": 2, "parent_id": None},
        {"competition_id": 115, "competition_name": "Challenger Torino", "type": "singles", "gender": "men", "category_id": 5, "parent_id": None},
    ])

    complexes_df = pd.DataFrame([
        {"complex_id": 1, "complex_name": "Melbourne Park"},
        {"complex_id": 2, "complex_name": "Stade Roland Garros"},
        {"complex_id": 3, "complex_name": "All England Club"},
        {"complex_id": 4, "complex_name": "USTA Billie Jean King National Tennis Center"},
        {"complex_id": 5, "complex_name": "Nacional"},
        {"complex_id": 6, "complex_name": "Foro Italico"},
        {"complex_id": 7, "complex_name": "Caja Mágica"},
        {"complex_id": 8, "complex_name": "Indian Wells Tennis Garden"}
    ])

    venues_df = pd.DataFrame([
        {"venue_id": 1, "venue_name": "Rod Laver Arena", "city_name": "Melbourne", "country_name": "Australia", "country_code": "AUS", "timezone": "Australia/Melbourne", "complex_id": 1},
        {"venue_id": 2, "venue_name": "Margaret Court Arena", "city_name": "Melbourne", "country_name": "Australia", "country_code": "AUS", "timezone": "Australia/Melbourne", "complex_id": 1},
        {"venue_id": 3, "venue_name": "Court Philippe-Chatrier", "city_name": "Paris", "country_name": "France", "country_code": "FRA", "timezone": "Europe/Paris", "complex_id": 2},
        {"venue_id": 4, "venue_name": "Court Suzanne-Lenglen", "city_name": "Paris", "country_name": "France", "country_code": "FRA", "timezone": "Europe/Paris", "complex_id": 2},
        {"venue_id": 5, "venue_name": "Centre Court", "city_name": "London", "country_name": "United Kingdom", "country_code": "GBR", "timezone": "Europe/London", "complex_id": 3},
        {"venue_id": 6, "venue_name": "Arthur Ashe Stadium", "city_name": "New York", "country_name": "United States", "country_code": "USA", "timezone": "America/New_York", "complex_id": 4},
        {"venue_id": 7, "venue_name": "Estadio Nacional Court 1", "city_name": "Santiago", "country_name": "Chile", "country_code": "CHI", "timezone": "America/Santiago", "complex_id": 5},
        {"venue_id": 8, "venue_name": "Estadio Nacional Court 2", "city_name": "Santiago", "country_name": "Chile", "country_code": "CHI", "timezone": "America/Santiago", "complex_id": 5},
        {"venue_id": 9, "venue_name": "Campo Centrale", "city_name": "Rome", "country_name": "Italy", "country_code": "ITA", "timezone": "Europe/Rome", "complex_id": 6},
        {"venue_id": 10, "venue_name": "Manolo Santana Stadium", "city_name": "Madrid", "country_name": "Spain", "country_code": "ESP", "timezone": "Europe/Madrid", "complex_id": 7},
        {"venue_id": 11, "venue_name": "Stadium 1", "city_name": "Indian Wells", "country_name": "United States", "country_code": "USA", "timezone": "America/Los_Angeles", "complex_id": 8},
        {"venue_id": 12, "venue_name": "Zagreb Central Court", "city_name": "Zagreb", "country_name": "Croatia", "country_code": "CRO", "timezone": "Europe/Zagreb", "complex_id": None}
    ])

    competitors_df = pd.DataFrame([
        {"competitor_id": 1001, "name": "Novak Djokovic", "country": "Serbia", "country_code": "SRB"},
        {"competitor_id": 1002, "name": "Carlos Alcaraz", "country": "Spain", "country_code": "ESP"},
        {"competitor_id": 1003, "name": "Jannik Sinner", "country": "Italy", "country_code": "ITA"},
        {"competitor_id": 1004, "name": "Daniil Medvedev", "country": "Russia", "country_code": "RUS"},
        {"competitor_id": 1005, "name": "Alexander Zverev", "country": "Germany", "country_code": "GER"},
        {"competitor_id": 1006, "name": "Andrey Rublev", "country": "Russia", "country_code": "RUS"},
        {"competitor_id": 1007, "name": "Holger Rune", "country": "Denmark", "country_code": "DEN"},
        {"competitor_id": 1008, "name": "Hubert Hurkacz", "country": "Poland", "country_code": "POL"},
        {"competitor_id": 1009, "name": "Matteo Berrettini", "country": "Italy", "country_code": "ITA"},
        {"competitor_id": 1010, "name": "Borna Coric", "country": "Croatia", "country_code": "CRO"},
        {"competitor_id": 1011, "name": "Marin Cilic", "country": "Croatia", "country_code": "CRO"},
        {"competitor_id": 1012, "name": "Nicolas Jarry", "country": "Chile", "country_code": "CHI"}
    ])

    rankings_df = pd.DataFrame([
        {"competitor_id": 1001, "rank": 1, "movement": 0, "points": 9855, "competitions_played": 18},
        {"competitor_id": 1002, "rank": 2, "movement": 1, "points": 8805, "competitions_played": 17},
        {"competitor_id": 1003, "rank": 3, "movement": 2, "points": 8270, "competitions_played": 16},
        {"competitor_id": 1004, "rank": 4, "movement": -1, "points": 7715, "competitions_played": 20},
        {"competitor_id": 1005, "rank": 5, "movement": 0, "points": 5030, "competitions_played": 22},
        {"competitor_id": 1006, "rank": 6, "movement": -1, "points": 5000, "competitions_played": 23},
        {"competitor_id": 1007, "rank": 7, "movement": 0, "points": 3700, "competitions_played": 21},
        {"competitor_id": 1008, "rank": 8, "movement": 3, "points": 3595, "competitions_played": 24},
        {"competitor_id": 1009, "rank": 9, "movement": 0, "points": 2800, "competitions_played": 15},
        {"competitor_id": 1010, "rank": 10, "movement": -2, "points": 2400, "competitions_played": 19},
        {"competitor_id": 1011, "rank": 11, "movement": 0, "points": 2100, "competitions_played": 14},
        {"competitor_id": 1012, "rank": 12, "movement": 1, "points": 1800, "competitions_played": 18}
    ])

    return categories_df, competitions_df, complexes_df, venues_df, competitors_df, rankings_df

categories_df, competitions_df, complexes_df, venues_df, competitors_df, rankings_df = load_data()

# Helper for standard Plotly charts layout styling
def apply_chart_theme(fig, height=400):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Inter, sans-serif", color="#334155", size=12),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title_font=dict(size=12, color="#64748B")),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title_font=dict(size=12, color="#64748B")),
        hoverlabel=dict(bgcolor="#0F172A", font_size=13, font_family="Inter, sans-serif")
    )
    return fig

# Custom Metric Component Helper
def display_kpi(label: str, value: str):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0;">
            <div style="font-size: 22px; font-weight: 800; letter-spacing: -0.5px;">🎾 Tennis Studio</div>
            <div style="font-size: 12px; opacity: 0.7; margin-top: 2px;">Sportradar Data Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            NAV_OVERVIEW,
            NAV_COMPETITIONS,
            NAV_VENUES,
            NAV_RANKINGS
        ],
        index=0
    )

    st.markdown("---")
    
    st.markdown('<span class="status-badge status-success">● Data Ready</span>', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size:12px; color:#94A3B8; margin-top: 30px;">
        <b>Engine:</b> Streamlit + Pandas<br>
        <b>Provider:</b> Sportradar Tennis API
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ============================================================
if page == NAV_OVERVIEW:
    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">Executive Game Analytics Overview</div>
            <div class="main-subtitle">Comprehensive data overview across global tennis competitions, venues, and players.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    total_categories = len(categories_df)
    total_competitions = len(competitions_df)
    total_venues = len(venues_df)
    total_competitors = len(competitors_df)
    total_countries = competitors_df["country"].nunique()
    highest_points = int(rankings_df["points"].max())

    st.markdown('<div class="section-header">📊 Executive Overview Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1: display_kpi("Competitions", f"{total_competitions:,}")
    with col2: display_kpi("Categories", f"{total_categories:,}")
    with col3: display_kpi("Competitors", f"{total_competitors:,}")
    with col4: display_kpi("Venues", f"{total_venues:,}")
    with col5: display_kpi("Countries", f"{total_countries:,}")
    with col6: display_kpi("Top Score", f"{highest_points:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Competitions by Category Chart
    st.markdown('<div class="section-header">🏆 Top Categories by Number of Competitions</div>', unsafe_allow_html=True)
    competition_category_df = categories_df.merge(competitions_df, on="category_id", how="left") \
        .groupby(["category_id", "category_name"], as_index=False) \
        .agg(total_competitions=("competition_id", "count")) \
        .sort_values(by="total_competitions", ascending=False).head(10)

    if not competition_category_df.empty:
        fig_category = px.bar(
            competition_category_df,
            x="category_name",
            y="total_competitions",
            text_auto=True,
            color="total_competitions",
            color_continuous_scale="Blues",
            labels={"category_name": "Category", "total_competitions": "Competitions"}
        )
        fig_category.update_coloraxes(showscale=False)
        apply_chart_theme(fig_category, height=380)
        st.plotly_chart(fig_category, use_container_width=True)

    # 2. Two Column Geographical Layout
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown('<div class="section-header">🌍 Top 10 Countries by Venue Count</div>', unsafe_allow_html=True)
        venue_country_df = venues_df.groupby("country_name", as_index=False) \
            .agg(total_venues=("venue_id", "count")) \
            .sort_values(by="total_venues", ascending=False).head(10)

        if not venue_country_df.empty:
            fig_venues = px.bar(
                venue_country_df,
                x="total_venues",
                y="country_name",
                orientation="h",
                text_auto=True,
                color="total_venues",
                color_continuous_scale="Teal",
                labels={"country_name": "Country", "total_venues": "Venues"}
            )
            fig_venues.update_coloraxes(showscale=False)
            fig_venues.update_layout(yaxis=dict(autorange="reversed"))
            apply_chart_theme(fig_venues, height=380)
            st.plotly_chart(fig_venues, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">🎾 Top 10 Countries by Competitor Count</div>', unsafe_allow_html=True)
        competitor_country_df = competitors_df.groupby("country", as_index=False) \
            .agg(total_competitors=("competitor_id", "count")) \
            .sort_values(by="total_competitors", ascending=False).head(10)

        if not competitor_country_df.empty:
            fig_competitors = px.bar(
                competitor_country_df,
                x="total_competitors",
                y="country",
                orientation="h",
                text_auto=True,
                color="total_competitors",
                color_continuous_scale="Viridis",
                labels={"country": "Country", "total_competitors": "Competitors"}
            )
            fig_competitors.update_coloraxes(showscale=False)
            fig_competitors.update_layout(yaxis=dict(autorange="reversed"))
            apply_chart_theme(fig_competitors, height=380)
            st.plotly_chart(fig_competitors, use_container_width=True)

    # 3. Top Ranked Competitors
    st.markdown('<div class="section-header">⭐ Top 10 Competitors by Ranking Points</div>', unsafe_allow_html=True)
    top_competitors_df = competitors_df.merge(rankings_df, on="competitor_id") \
        [["name", "country", "rank", "points"]] \
        .sort_values(by="points", ascending=False).head(10)

    if not top_competitors_df.empty:
        st.dataframe(
            top_competitors_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "points": st.column_config.ProgressColumn(
                    "Points",
                    format="%d",
                    min_value=0,
                    max_value=int(top_competitors_df["points"].max())
                )
            }
        )

# ============================================================
# PAGE 2: COMPETITIONS
# ============================================================
elif page == NAV_COMPETITIONS:
    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">Competition Analytics</div>
            <div class="main-subtitle">Explore tennis competitions, categories, formats, and hierarchy.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    t_comp = len(competitions_df)
    t_cat = len(categories_df)
    t_dbl = len(competitions_df[competitions_df["competition_name"].str.lower().str.contains("doubles", na=False)])
    t_par = len(competitions_df[competitions_df["parent_id"].isna()])

    col1, col2, col3, col4 = st.columns(4)
    with col1: display_kpi("Total Competitions", f"{t_comp:,}")
    with col2: display_kpi("Categories", f"{t_cat:,}")
    with col3: display_kpi("Doubles Events", f"{t_dbl:,}")
    with col4: display_kpi("Top-Level Events", f"{t_par:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "📋 All Competitions",
            "📊 By Category",
            "🎾 Doubles",
            "🔎 Category Search",
            "🔗 Parent / Sub",
            "📈 Type Distribution",
            "🏆 Top-Level"
        ]
    )

    merged_comp_df = competitions_df.merge(categories_df, on="category_id", how="left")

    with tab1:
        st.markdown('<div class="section-header">📋 All Competitions with Category</div>', unsafe_allow_html=True)
        all_comp_df = merged_comp_df[["competition_id", "competition_name", "type", "gender", "category_name"]] \
            .sort_values(by="competition_name")

        if not all_comp_df.empty:
            search = st.text_input("🔍 Search competition", placeholder="Enter competition name...", key="tab1_search")
            filtered_df = all_comp_df[all_comp_df["competition_name"].str.contains(search, case=False, na=False)] if search else all_comp_df
            st.caption(f"Showing {len(filtered_df):,} of {len(all_comp_df):,} competitions")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown('<div class="section-header">📊 Competitions per Category</div>', unsafe_allow_html=True)
        cat_comp_df = categories_df.merge(competitions_df, on="category_id", how="left") \
            .groupby(["category_id", "category_name"], as_index=False) \
            .agg(total_competitions=("competition_id", "count")) \
            .sort_values(by="total_competitions", ascending=False)

        if not cat_comp_df.empty:
            fig = px.bar(
                cat_comp_df.head(15),
                x="total_competitions",
                y="category_name",
                orientation="h",
                text_auto=True,
                color="total_competitions",
                color_continuous_scale="Blues",
                labels={"total_competitions": "Competitions", "category_name": "Category"}
            )
            fig.update_coloraxes(showscale=False)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            apply_chart_theme(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown('<div class="section-header">🎾 Doubles Competitions</div>', unsafe_allow_html=True)
        doubles_df = merged_comp_df[merged_comp_df["competition_name"].str.lower().str.contains("doubles", na=False)] \
            [["competition_id", "competition_name", "type", "gender", "category_name"]] \
            .sort_values(by="competition_name")

        if not doubles_df.empty:
            st.metric("Doubles Competitions Found", f"{len(doubles_df):,}")
            st.dataframe(doubles_df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown('<div class="section-header">🔎 Competitions by Selected Category</div>', unsafe_allow_html=True)
        category_names = sorted(categories_df["category_name"].dropna().unique().tolist())
        if category_names:
            default_idx = category_names.index("ITF Men") if "ITF Men" in category_names else 0
            selected_category = st.selectbox("Select a category", category_names, index=default_idx)
            
            sel_cat_df = merged_comp_df[merged_comp_df["category_name"] == selected_category] \
                [["competition_id", "competition_name", "type", "gender", "category_name"]] \
                .sort_values(by="competition_name")
            st.dataframe(sel_cat_df, use_container_width=True, hide_index=True)

    with tab5:
        st.markdown('<div class="section-header">🔗 Parent and Sub-Competitions</div>', unsafe_allow_html=True)
        hierarchy_df = competitions_df[competitions_df["parent_id"].notna()].merge(
            competitions_df, left_on="parent_id", right_on="competition_id", suffixes=("", "_parent")
        )
        hierarchy_df = hierarchy_df.rename(columns={
            "competition_name": "sub_competition",
            "competition_name_parent": "parent_competition"
        })[["competition_id", "sub_competition", "parent_competition", "type", "gender"]] \
          .sort_values(by=["parent_competition", "sub_competition"])

        if not hierarchy_df.empty:
            st.dataframe(hierarchy_df, use_container_width=True, hide_index=True)

    with tab6:
        st.markdown('<div class="section-header">📈 Competition Type Distribution by Category</div>', unsafe_allow_html=True)
        type_dist_df = merged_comp_df.groupby(["category_name", "type"], as_index=False) \
            .agg(total_competitions=("competition_id", "count")) \
            .sort_values(by=["category_name", "total_competitions"], ascending=[True, False])

        if not type_dist_df.empty:
            category_filter = st.multiselect("Filter categories", sorted(type_dist_df["category_name"].dropna().unique()), default=[])
            if category_filter:
                chart_df = type_dist_df[type_dist_df["category_name"].isin(category_filter)]
            else:
                top_cats = type_dist_df.groupby("category_name")["total_competitions"].sum().nlargest(10).index
                chart_df = type_dist_df[type_dist_df["category_name"].isin(top_cats)]

            fig = px.bar(
                chart_df,
                x="category_name",
                y="total_competitions",
                color="type",
                barmode="stack",
                labels={"category_name": "Category", "total_competitions": "Competitions", "type": "Type"}
            )
            apply_chart_theme(fig, height=480)
            st.plotly_chart(fig, use_container_width=True)

    with tab7:
        st.markdown('<div class="section-header">🏆 Top-Level Competitions</div>', unsafe_allow_html=True)
        top_level_df = merged_comp_df[merged_comp_df["parent_id"].isna()] \
            [["competition_id", "competition_name", "type", "gender", "category_name"]] \
            .sort_values(by="competition_name")

        if not top_level_df.empty:
            st.dataframe(top_level_df, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 3: VENUES & LOGISTICS
# ============================================================
elif page == NAV_VENUES:
    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">Venues & Geographical Logistics</div>
            <div class="main-subtitle">Explore tennis venues, sports complexes, geographical distribution and timezones.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    t_c = len(complexes_df)
    t_v = len(venues_df)
    t_cntry = venues_df["country_name"].nunique()
    t_tz = venues_df["timezone"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1: display_kpi("Complexes", f"{t_c:,}")
    with col2: display_kpi("Venues", f"{t_v:,}")
    with col3: display_kpi("Countries", f"{t_cntry:,}")
    with col4: display_kpi("Timezones", f"{t_tz:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "📋 All Venues",
            "📊 Venues per Complex",
            "🌎 Country Search",
            "🕐 Timezones",
            "🏟️ Multi-Venue Complexes",
            "🌍 By Country",
            "🔎 Complex Search"
        ]
    )

    merged_venues_df = venues_df.merge(complexes_df, on="complex_id", how="left")

    with tab1:
        st.markdown('<div class="section-header">📋 All Venues with Associated Complex</div>', unsafe_allow_html=True)
        venues_display_df = merged_venues_df[["venue_id", "venue_name", "city_name", "country_name", "country_code", "timezone", "complex_name"]] \
            .sort_values(by="venue_name")

        if not venues_display_df.empty:
            search_v = st.text_input("🔍 Search venue", placeholder="Enter venue name...", key="v_search")
            filtered_v = venues_display_df[venues_display_df["venue_name"].str.contains(search_v, case=False, na=False)] if search_v else venues_display_df
            st.dataframe(filtered_v, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown('<div class="section-header">📊 Number of Venues in Each Complex</div>', unsafe_allow_html=True)
        v_per_c_df = complexes_df.merge(venues_df, on="complex_id", how="left") \
            .groupby(["complex_id", "complex_name"], as_index=False) \
            .agg(total_venues=("venue_id", "count")) \
            .sort_values(by="total_venues", ascending=False)

        if not v_per_c_df.empty:
            fig = px.bar(
                v_per_c_df.head(15),
                x="total_venues",
                y="complex_name",
                orientation="h",
                text_auto=True,
                color="total_venues",
                color_continuous_scale="Tealgrn"
            )
            fig.update_coloraxes(showscale=False)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            apply_chart_theme(fig, height=480)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown('<div class="section-header">🌎 Venues in a Specific Country</div>', unsafe_allow_html=True)
        countries = sorted(venues_df["country_name"].dropna().unique().tolist())
        if countries:
            default_c = countries.index("Chile") if "Chile" in countries else 0
            selected_country = st.selectbox("Select country", countries, index=default_c)
            
            c_venues_df = merged_venues_df[merged_venues_df["country_name"] == selected_country] \
                [["venue_id", "venue_name", "city_name", "country_name", "country_code", "timezone", "complex_name"]] \
                .sort_values(by="venue_name")
            st.dataframe(c_venues_df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown('<div class="section-header">🕐 Venues and Their Timezones</div>', unsafe_allow_html=True)
        timezone_df = venues_df[["venue_name", "city_name", "country_name", "timezone"]] \
            .sort_values(by=["timezone", "venue_name"])

        if not timezone_df.empty:
            tz_filter = st.multiselect("Filter by timezone", sorted(timezone_df["timezone"].dropna().unique()))
            filtered_tz = timezone_df[timezone_df["timezone"].isin(tz_filter)] if tz_filter else timezone_df
            st.dataframe(filtered_tz, use_container_width=True, hide_index=True)

    with tab5:
        st.markdown('<div class="section-header">🏟️ Complexes with More Than One Venue</div>', unsafe_allow_html=True)
        multi_venue_df = complexes_df.merge(venues_df, on="complex_id", how="inner") \
            .groupby(["complex_id", "complex_name"], as_index=False) \
            .agg(total_venues=("venue_id", "count"))
        multi_venue_df = multi_venue_df[multi_venue_df["total_venues"] > 1].sort_values(by="total_venues", ascending=False)

        if not multi_venue_df.empty:
            fig = px.bar(
                multi_venue_df.head(15),
                x="total_venues",
                y="complex_name",
                orientation="h",
                text_auto=True,
                color="total_venues",
                color_continuous_scale="Blues"
            )
            fig.update_coloraxes(showscale=False)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            apply_chart_theme(fig, height=450)
            st.plotly_chart(fig, use_container_width=True)

    with tab6:
        st.markdown('<div class="section-header">🌍 Venues Grouped by Country</div>', unsafe_allow_html=True)
        c_group_df = venues_df.groupby(["country_name", "country_code"], as_index=False) \
            .agg(total_venues=("venue_id", "count")) \
            .sort_values(by="total_venues", ascending=False)

        if not c_group_df.empty:
            fig = px.bar(
                c_group_df.head(20),
                x="total_venues",
                y="country_name",
                orientation="h",
                text_auto=True,
                color="total_venues",
                color_continuous_scale="Viridis"
            )
            fig.update_coloraxes(showscale=False)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            apply_chart_theme(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)

    with tab7:
        st.markdown('<div class="section-header">🔎 Venues for a Specific Complex</div>', unsafe_allow_html=True)
        complex_names = sorted(complexes_df["complex_name"].dropna().unique().tolist())
        if complex_names:
            default_cmplx = complex_names.index("Nacional") if "Nacional" in complex_names else 0
            selected_complex = st.selectbox("Select complex", complex_names, index=default_cmplx)
            
            sel_cmplx_df = merged_venues_df[merged_venues_df["complex_name"] == selected_complex] \
                [["venue_id", "venue_name", "city_name", "country_name", "country_code", "timezone", "complex_name"]] \
                .sort_values(by="venue_name")
            st.dataframe(sel_cmplx_df, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 4: COMPETITOR RANKINGS
# ============================================================
elif page == NAV_RANKINGS:
    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">Player Rankings & Performance</div>
            <div class="main-subtitle">Explore doubles rankings, competitor performance, point distribution, and country insights.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    t_comp = len(competitors_df)
    t_cntry = competitors_df["country"].nunique()
    t_pts = int(rankings_df["points"].max())
    t_stbl = len(rankings_df[rankings_df["movement"] == 0])
    t_top5 = len(rankings_df[rankings_df["rank"] <= 5])

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: display_kpi("Competitors", f"{t_comp:,}")
    with col2: display_kpi("Countries", f"{t_cntry:,}")
    with col3: display_kpi("Highest Points", f"{t_pts:,}")
    with col4: display_kpi("Stable Ranks", f"{t_stbl:,}")
    with col5: display_kpi("Top 5 Players", f"{t_top5:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📋 All Rankings",
            "🏆 Top 5",
            "↔️ Stable Rank",
            "🌍 Country Analysis",
            "📊 Competitors by Country",
            "⭐ Highest Points"
        ]
    )

    merged_rankings_df = competitors_df.merge(rankings_df, on="competitor_id")

    with tab1:
        st.markdown('<div class="section-header">📋 Competitor Rankings Explorer</div>', unsafe_allow_html=True)
        all_rankings_df = merged_rankings_df[["competitor_id", "name", "country", "country_code", "rank", "movement", "points", "competitions_played"]] \
            .sort_values(by="rank")

        if not all_rankings_df.empty:
            c_f1, c_f2, c_f3 = st.columns(3)
            with c_f1: search_name = st.text_input("🔍 Search competitor", placeholder="Enter competitor name...", key="rank_s")
            with c_f2:
                countries = sorted(all_rankings_df["country"].dropna().unique().tolist())
                selected_countries = st.multiselect("🌍 Filter by country", countries)
            with c_f3:
                max_rank = int(all_rankings_df["rank"].max())
                rank_range = st.slider("🏆 Rank range", min_value=1, max_value=max_rank, value=(1, min(50, max_rank)))

            min_points = st.number_input("⭐ Minimum ranking points", min_value=0, max_value=int(all_rankings_df["points"].max()), value=0, step=100)

            filtered_df = all_rankings_df.copy()
            if search_name: filtered_df = filtered_df[filtered_df["name"].str.contains(search_name, case=False, na=False)]
            if selected_countries: filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]
            filtered_df = filtered_df[(filtered_df["rank"] >= rank_range[0]) & (filtered_df["rank"] <= rank_range[1]) & (filtered_df["points"] >= min_points)]

            st.caption(f"Showing {len(filtered_df):,} of {len(all_rankings_df):,} competitors")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "points": st.column_config.ProgressColumn("points", format="%d", min_value=0, max_value=int(all_rankings_df["points"].max())),
                    "movement": st.column_config.NumberColumn("movement", format="%+d")
                }
            )

    with tab2:
        st.markdown('<div class="section-header">🏆 Top 5 Competitors</div>', unsafe_allow_html=True)
        top_five_df = merged_rankings_df[merged_rankings_df["rank"] <= 5] \
            [["competitor_id", "name", "country", "rank", "movement", "points", "competitions_played"]] \
            .sort_values(by="rank")

        if not top_five_df.empty:
            st.dataframe(top_five_df, use_container_width=True, hide_index=True)
            fig = px.bar(
                top_five_df,
                x="name",
                y="points",
                text_auto=True,
                color="points",
                color_continuous_scale="Blues",
                labels={"name": "Competitor", "points": "Ranking Points"},
                hover_data=["country", "rank", "movement"]
            )
            fig.update_coloraxes(showscale=False)
            apply_chart_theme(fig, height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown('<div class="section-header">↔️ Competitors with No Rank Movement</div>', unsafe_allow_html=True)
        stable_df = merged_rankings_df[merged_rankings_df["movement"] == 0] \
            [["competitor_id", "name", "country", "rank", "movement", "points", "competitions_played"]] \
            .sort_values(by="rank")

        if not stable_df.empty:
            search_stable = st.text_input("🔍 Search stable competitor", placeholder="Enter competitor name...", key="stable_search")
            display_stable_df = stable_df[stable_df["name"].str.contains(search_stable, case=False, na=False)] if search_stable else stable_df
            st.dataframe(display_stable_df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown('<div class="section-header">🌍 Country-Wise Ranking Points</div>', unsafe_allow_html=True)
        countries = sorted(competitors_df["country"].dropna().unique().tolist())
        if countries:
            default_cntry = countries.index("Croatia") if "Croatia" in countries else 0
            selected_country = st.selectbox("Select country", countries, index=default_cntry, key="c_pts_select")
            
            country_competitors_df = merged_rankings_df[merged_rankings_df["country"] == selected_country] \
                [["name", "country", "rank", "movement", "points", "competitions_played"]] \
                .sort_values(by="rank")

            if not country_competitors_df.empty:
                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1: display_kpi("Competitors", f"{len(country_competitors_df):,}")
                with col_c2: display_kpi("Total Points", f"{int(country_competitors_df['points'].sum()):,}")
                with col_c3: display_kpi("Average Points", f"{country_competitors_df['points'].mean():,.0f}")
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(country_competitors_df, use_container_width=True, hide_index=True)

    with tab5:
        st.markdown('<div class="section-header">📊 Competitors by Country</div>', unsafe_allow_html=True)
        competitors_country_df = competitors_df.groupby("country", as_index=False) \
            .agg(total_competitors=("competitor_id", "count")) \
            .sort_values(by="total_competitors", ascending=False)

        if not competitors_country_df.empty:
            fig = px.bar(
                competitors_country_df.head(20),
                x="total_competitors",
                y="country",
                orientation="h",
                text_auto=True,
                color="total_competitors",
                color_continuous_scale="Viridis"
            )
            fig.update_coloraxes(showscale=False)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            apply_chart_theme(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)

    with tab6:
        st.markdown('<div class="section-header">⭐ Highest Ranking Points</div>', unsafe_allow_html=True)
        max_points = int(rankings_df["points"].max())
        highest_competitors_df = merged_rankings_df[merged_rankings_df["points"] == max_points] \
            [["competitor_id", "name", "country", "rank", "movement", "points", "competitions_played"]] \
            .sort_values(by="rank")

        st.metric("Highest Ranking Points Standard", f"{max_points:,}")
        st.dataframe(highest_competitors_df, use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94A3B8; font-size: 13px; padding-bottom: 20px;">
        Tennis Game Analytics Studio • Powered by Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True
)