import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Netflix-style design
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body, [data-testid="stAppViewContainer"] {
        background-color: #0f0f0f !important;
        color: #e5e5e5 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #141414 !important;
        border-right: 3px solid #e50914 !important;
    }
    
    [data-testid="stSidebar"] > div > div {
        background-color: #141414 !important;
    }
    
    .stTabs [role="tablist"] {
        gap: 8px;
        border-bottom: 2px solid #e50914;
    }
    
    .stTabs [role="tab"] {
        background-color: #1a1a1a;
        border-radius: 8px 8px 0 0;
        color: #b3b3b3;
        padding: 12px 24px;
        font-weight: bold;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #e50914;
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #e5e5e5 !important;
        font-weight: 700 !important;
    }
    
    .metric {
        background-color: #1a1a1a !important;
        border-left: 4px solid #e50914 !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }
    
    .stMetric {
        background-color: #1a1a1a;
        border-radius: 8px;
        border-left: 4px solid #e50914;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    .stButton > button {
        background-color: #e50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #b20710 !important;
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.4) !important;
    }
    
    .stSelectbox, .stMultiSelect, .stSlider {
        color: #e5e5e5 !important;
    }
    
    .stDataFrame {
        background-color: #1a1a1a !important;
    }
    
    p, label, span {
        color: #b3b3b3 !important;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 20px 0;
        border-bottom: 2px solid #e50914;
        margin-bottom: 20px;
    }
    
    .netflix-title {
        font-size: 32px !important;
        font-weight: bold !important;
        color: #e50914 !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        letter-spacing: 2px !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("netflix_titles.csv")

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h1 style="color: #e50914; font-size: 32px; margin: 0;">🎬 NETFLIX</h1></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #e5e5e5; margin: 20px 0 15px 0;">Filters & Controls</h3>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Content Type Filter
    st.markdown('<p style="color: #e50914; font-weight: bold; margin-bottom: 8px;">📺 Content Type</p>', unsafe_allow_html=True)
    type_filter = st.selectbox(
        "Select Type",
        options=["All"] + list(df["type"].unique()),
        label_visibility="collapsed",
        key="type_select"
    )
    
    # Rating Filter
    st.markdown('<p style="color: #e50914; font-weight: bold; margin-bottom: 8px; margin-top: 20px;">⭐ Content Rating</p>', unsafe_allow_html=True)
    rating_filter = st.multiselect(
        "Select Ratings",
        options=sorted(df["rating"].dropna().unique()),
        default=sorted(df["rating"].dropna().unique()),
        label_visibility="collapsed",
        key="rating_select"
    )
    
    # Year Range Filter
    st.markdown('<p style="color: #e50914; font-weight: bold; margin-bottom: 8px; margin-top: 20px;">📅 Release Year</p>', unsafe_allow_html=True)
    year_min, year_max = int(df["release_year"].min()), int(df["release_year"].max())
    year_filter = st.slider(
        "Select Year Range",
        year_min,
        year_max,
        (year_min, year_max),
        label_visibility="collapsed",
        key="year_slider"
    )
    
    st.markdown("---")
    
    # View Mode Selection
    st.markdown('<h4 style="color: #e5e5e5; margin: 20px 0 10px 0;">View Mode</h4>', unsafe_allow_html=True)
    view_mode = st.radio(
        "Choose view",
        ["📊 Dashboard", "📚 Full Dataset", "🔍 Search"],
        label_visibility="collapsed",
        key="view_mode"
    )

# Apply filters
filtered_df = df.copy()

if type_filter != "All":
    filtered_df = filtered_df[filtered_df["type"] == type_filter]

filtered_df = filtered_df[filtered_df["rating"].isin(rating_filter)]
filtered_df = filtered_df[(filtered_df["release_year"] >= year_filter[0]) & 
                          (filtered_df["release_year"] <= year_filter[1])]

# Main Content
if view_mode == "📊 Dashboard":
    st.markdown('<h1 class="netflix-title">📊 Netflix Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 Total Content",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df)} filtered"
        )
    
    with col2:
        movie_count = len(filtered_df[filtered_df["type"] == "Movie"])
        st.metric(label="🎬 Movies", value=f"{movie_count:,}")
    
    with col3:
        show_count = len(filtered_df[filtered_df["type"] == "TV Show"])
        st.metric(label="📺 TV Shows", value=f"{show_count:,}")
    
    with col4:
        countries = filtered_df["country"].dropna().str.split(", ").explode().nunique()
        st.metric(label="🌍 Countries", value=f"{countries:,}")
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        # Content Type Distribution
        type_data = filtered_df["type"].value_counts()
        fig1 = px.pie(
            values=type_data.values,
            names=type_data.index,
            title="📺 Content Type Distribution",
            color_discrete_sequence=["#e50914", "#221f1f"],
            hole=0.4
        )
        fig1.update_layout(
            paper_bgcolor="#0f0f0f",
            plot_bgcolor="#0f0f0f",
            font=dict(color="#e5e5e5", family="Arial", size=12),
            title_font_size=16,
            showlegend=True
        )
        st.plotly_chart(fig1, width='stretch')
    
    with col2:
        # Top Countries
        country_data = filtered_df["country"].dropna().str.split(", ").explode().value_counts().head(10)
        fig2 = px.bar(
            x=country_data.values,
            y=country_data.index,
            title="🌍 Top 10 Countries by Content",
            color_discrete_sequence=["#e50914"],
            orientation="h"
        )
        fig2.update_layout(
            paper_bgcolor="#0f0f0f",
            plot_bgcolor="#0f0f0f",
            font=dict(color="#e5e5e5", family="Arial", size=12),
            title_font_size=16,
            yaxis_autorange="reversed",
            xaxis_title="Number of Titles",
            yaxis_title=""
        )
        st.plotly_chart(fig2, width='stretch')
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Releases Over Time
        year_data = filtered_df["release_year"].value_counts().sort_index()
        fig3 = px.line(
            x=year_data.index,
            y=year_data.values,
            title="📈 Content Released Over Years",
            markers=True
        )
        fig3.update_traces(
            line=dict(color="#e50914", width=3),
            marker=dict(size=8, color="#e50914")
        )
        fig3.update_layout(
            paper_bgcolor="#0f0f0f",
            plot_bgcolor="#0f0f0f",
            font=dict(color="#e5e5e5", family="Arial", size=12),
            title_font_size=16,
            xaxis_title="Year",
            yaxis_title="Number of Titles",
            hovermode='x unified'
        )
        st.plotly_chart(fig3, width='stretch')
    
    with col4:
        # Ratings Distribution
        rating_data = filtered_df["rating"].value_counts()
        fig4 = px.bar(
            y=rating_data.index,
            x=rating_data.values,
            title="⭐ Content by Rating",
            color_discrete_sequence=["#e50914"]
        )
        fig4.update_layout(
            paper_bgcolor="#0f0f0f",
            plot_bgcolor="#0f0f0f",
            font=dict(color="#e5e5e5", family="Arial", size=12),
            title_font_size=16,
            xaxis_title="Count",
            yaxis_title="",
            yaxis_autorange="reversed"
        )
        st.plotly_chart(fig4, width='stretch')
    
    st.markdown("---")
    
    # Top Genres
    st.markdown('<h3 style="color: #e5e5e5; margin: 20px 0;">📽️ Top Genres</h3>', unsafe_allow_html=True)
    genres = filtered_df["listed_in"].dropna().str.split(", ").explode().value_counts().head(15)
    fig5 = px.bar(
        y=genres.index,
        x=genres.values,
        title="Top 15 Genres",
        color_discrete_sequence=["#e50914"]
    )
    fig5.update_layout(
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        font=dict(color="#e5e5e5", family="Arial", size=12),
        title_font_size=16,
        xaxis_title="Count",
        yaxis_title="",
        yaxis_autorange="reversed"
    )
    st.plotly_chart(fig5, width='stretch')

elif view_mode == "📚 Full Dataset":
    st.markdown('<h2 class="netflix-title">📚 Full Netflix Dataset</h2>', unsafe_allow_html=True)
    st.info(f"📊 Displaying {len(filtered_df):,} out of {len(df):,} titles")
    
    # Column selector
    col_select = st.multiselect(
        "Select columns to display",
        options=filtered_df.columns.tolist(),
        default=["title", "type", "release_year", "rating", "country", "listed_in"]
    )
    
    st.dataframe(
        filtered_df[col_select].sort_values("release_year", ascending=False),
        use_container_width=True,
        height=600
    )

else:  # Search Mode
    st.markdown('<h2 class="netflix-title">🔍 Search Netflix Content</h2>', unsafe_allow_html=True)
    
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_term = st.text_input("Search by title or description", placeholder="e.g., Stranger Things, Breaking Bad...")
    
    if search_term:
        search_results = filtered_df[
            (filtered_df["title"].str.contains(search_term, case=False, na=False)) |
            (filtered_df["description"].str.contains(search_term, case=False, na=False))
        ].sort_values("release_year", ascending=False)
        
        st.markdown(f"<p style='color: #e50914; font-weight: bold; font-size: 18px;'>Found {len(search_results)} results</p>", unsafe_allow_html=True)
        
        if len(search_results) > 0:
            for idx, row in search_results.head(10).iterrows():
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        st.markdown(f"<h4 style='color: #e50914; margin: 0;'>{row['type']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #b3b3b3; margin: 5px 0;'>⭐ {row['rating']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #b3b3b3; margin: 0;'>📅 {row['release_year']}</p>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"<h3 style='color: #e5e5e5; margin-top: 0;'>{row['title']}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #b3b3b3; margin: 10px 0;'>{row['description'][:200]}...</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #808080; font-size: 12px;'>📍 {row['country']} | 🎭 {row['listed_in']}</p>", unsafe_allow_html=True)
                    
                    st.markdown("---")
        else:
            st.warning("No results found. Try a different search term.")
