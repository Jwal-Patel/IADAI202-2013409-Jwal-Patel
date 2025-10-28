"""
🏆 FOOTBALL INJURY IMPACT DASHBOARD - ENHANCED VERSION WITH IMPROVED DESIGN
========================================================
A comprehensive, production-ready Streamlit application for analyzing player injuries 
and their impact on team performance. IMPROVED VERSION with better styling and layout.

Company: FootLens Analytics
Role: Junior Sports Data Analyst
Assignment: Developing User-Centered Dashboards to Solve Real-World Problems
Course: Mathematics for AI-II (IBDP)

Author: AI Data Analytics Team
Last Updated: October 2025
Version: 2.1 (Enhanced Design)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
from scipy import stats
from io import BytesIO

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION & THEMING
# ============================================================================
st.set_page_config(
    page_title="Football Injury Impact Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom theme colors
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
SUCCESS_COLOR = "#2ca02c"
DANGER_COLOR = "#d62728"
WARNING_COLOR = "#ff9896"
INFO_COLOR = "#17becf"

# ============================================================================
# PROFESSIONAL STYLING & BRANDING - IMPROVED VERSION
# ============================================================================
st.markdown("""
    <style>
    :root {{
        --primary-color: {PRIMARY_COLOR};
        --secondary-color: {SECONDARY_COLOR};
        --success-color: {SUCCESS_COLOR};
        --danger-color: {DANGER_COLOR};
    }}
    
    /* Main Header - Fixed and improved visibility */
    .main-header {{
        font-size: 3.5rem;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        margin: 20px 0 10px 0;
        padding: 20px;
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        border-radius: 15px;
        text-align: center;
        letter-spacing: 1px;
    }}
    
    .football {{
        font-size: 4rem;
        animation: bounce 1s infinite;
    }}
    
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}

    /* Tab styling */
    .tab-header {{
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
        margin: 20px 0 20px 0;
        border-bottom: 4px solid {SECONDARY_COLOR};
        padding: 15px 20px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, transparent);
        border-radius: 10px 10px 0 0;
    }}
    
    /* Question styling - IMPROVED VISIBILITY */
    .question-box {{
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, {DANGER_COLOR} 0%, {WARNING_COLOR} 100%);
        padding: 20px 25px;
        margin: 20px 0;
        border-radius: 12px;
        border-left: 8px solid {SECONDARY_COLOR};
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    
    /* Metric cards */
    .metric-card {{
        background: linear-gradient(135deg, #f0f2f6 0%, #e8eef7 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {PRIMARY_COLOR};
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }}
    
    /* Q&A Section styling */
    .qa-section {{
        margin: 20px 0;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border-left: 5px solid {INFO_COLOR};
    }}
    
    /* Title fix for questions */
    h3 {{
        color: {PRIMARY_COLOR};
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 10px;
    }}

    .answer-box, .insight-box, .stat-highlight {{
        background: #f9fcff !important;
        color: #232629 !important;
        font-weight: 600;
        border-radius: 12px;
        border-left: 4px solid #3498db;
        margin: 12px 0 !important;
        padding: 18px 20px !important;
        box-shadow: none !important;
    }}
            
    .stat-highlight {{
        display: inline-block;
        background: #e2f2fc !important;
        color: #174066 !important;
        padding: 9px 14px 7px 14px;
        border-radius: 7px;
        font-size: 1.15rem;
        margin-right: 10px;
        font-weight: bold;
    }}
    
    .footer {{
        background: none !important;
        color: #909398 !important;
        border-radius: 0 !important;
        padding: 18px 0 10px 0 !important;
        text-align: center !important;
        box-shadow: none !important;
        border-top: 1.5px solid #ededed !important;
        font-size: 0.97rem !important;
        margin-top: 26px !important;
    }}
            
    .sub-header {{
        background: none !important;
        color: #868e96 !important;
        text-align: center !important;
        font-weight: 400 !important;
        font-size: 1.13rem !important;
        margin-bottom: 16px !important;
        border: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }}
            
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & ADVANCED PREPROCESSING
# ============================================================================
@st.cache_data
def load_and_preprocess_data():
    """
    Advanced data preprocessing pipeline with comprehensive feature engineering.
    """
    try:
        df = pd.read_csv('player_injuries_impact.csv')
        
        # Date processing
        df['Date of Injury'] = pd.to_datetime(df['Date of Injury'], errors='coerce')
        df['Date of return'] = pd.to_datetime(df['Date of return'], errors='coerce')
        
        df['Injury_Duration_Days'] = (df['Date of return'] - df['Date of Injury']).dt.days
        df['Injury_Duration_Days'] = df['Injury_Duration_Days'].fillna(df['Injury_Duration_Days'].median())
        
        df['Injury_Month'] = df['Date of Injury'].dt.month
        df['Injury_Year'] = df['Date of Injury'].dt.year
        df['Injury_Month_Name'] = df['Date of Injury'].dt.strftime('%B')
        df['Injury_Quarter'] = df['Date of Injury'].dt.quarter
        df['Injury_Week'] = df['Date of Injury'].dt.isocalendar().week
        
        # Value cleaning
        def clean_rating(val):
            if val == 'N.A.' or pd.isna(val):
                return np.nan
            try:
                return float(str(val).replace('(S)', '').replace('(A)', '').strip())
            except:
                return np.nan
        
        def clean_gd(val):
            if val == 'N.A.' or pd.isna(val):
                return np.nan
            try:
                return float(val)
            except:
                return np.nan
        
        rating_cols = [col for col in df.columns if 'Player_rating' in col]
        for col in rating_cols:
            df[col] = df[col].apply(clean_rating)
        
        gd_cols = [col for col in df.columns if '_GD' in col]
        for col in gd_cols:
            df[col] = df[col].apply(clean_gd)
        
        # Feature engineering
        before_rating_cols = ['Match1_before_injury_Player_rating', 'Match2_before_injury_Player_rating', 'Match3_before_injury_Player_rating']
        after_rating_cols = ['Match1_after_injury_Player_rating', 'Match2_after_injury_Player_rating', 'Match3_after_injury_Player_rating']
        
        df['Avg_Rating_Before_Injury'] = df[before_rating_cols].mean(axis=1)
        df['Avg_Rating_After_Injury'] = df[after_rating_cols].mean(axis=1)
        df['Performance_Drop_Index'] = df['Avg_Rating_Before_Injury'] - df['Avg_Rating_After_Injury']
        df['Performance_Recovery_Rate'] = (df['Performance_Drop_Index'] / (df['Avg_Rating_Before_Injury'] + 0.001)) * 100
        
        missed_gd_cols = ['Match1_missed_match_GD', 'Match2_missed_match_GD', 'Match3_missed_match_GD']
        before_gd_cols = ['Match1_before_injury_GD', 'Match2_before_injury_GD', 'Match3_before_injury_GD']
        after_gd_cols = ['Match1_after_injury_GD', 'Match2_after_injury_GD', 'Match3_after_injury_GD']
        
        df['Avg_GD_Before'] = df[before_gd_cols].mean(axis=1)
        df['Team_Performance_During_Absence'] = df[missed_gd_cols].mean(axis=1)
        df['Avg_GD_After'] = df[after_gd_cols].mean(axis=1)
        df['Team_Performance_Drop'] = df['Avg_GD_Before'] - df['Team_Performance_During_Absence']
        
        df['Win_Ratio_Before'] = (df['Match1_before_injury_Result'] == 'win').astype(int) + \
                                 (df['Match2_before_injury_Result'] == 'win').astype(int) + \
                                 (df['Match3_before_injury_Result'] == 'win').astype(int)
        
        df['Win_Ratio_During'] = (df['Match1_missed_match_Result'] == 'win').astype(int) + \
                                 (df['Match2_missed_match_Result'] == 'win').astype(int) + \
                                 (df['Match3_missed_match_Result'] == 'win').astype(int)
        
        # Injury severity
        def categorize_severity(injury_type):
            severe_keywords = ['cruciate', 'acl', 'meniscus', 'fracture', 'rupture', 'tear', 'ligament']
            moderate_keywords = ['hamstring', 'groin', 'calf', 'shoulder', 'ankle', 'strain']
            
            injury_lower = injury_type.lower()
            for keyword in severe_keywords:
                if keyword in injury_lower:
                    return 'Severe'
            for keyword in moderate_keywords:
                if keyword in injury_lower:
                    return 'Moderate'
            return 'Minor'
        
        df['Injury_Severity'] = df['Injury'].apply(categorize_severity)
        
        df['Recovery_Index'] = df['Injury_Duration_Days'] / 100
        df['Team_Impact_Severity'] = abs(df['Team_Performance_Drop']) * np.where(df['Injury_Severity'] == 'Severe', 1.5,
                                        np.where(df['Injury_Severity'] == 'Moderate', 1.0, 0.7))
        
        df['Age_Group'] = pd.cut(df['Age'], bins=[0, 23, 26, 29, 40], 
                                 labels=['Young (≤23)', 'Prime (24-26)', 'Experienced (27-29)', 'Veteran (30+)'])
        
        df['Performance_Category'] = pd.cut(df['FIFA rating'], 
                                           bins=[0, 75, 80, 85, 100],
                                           labels=['Average', 'Good', 'Very Good', 'Elite'])
        
        # Missing value handling
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
df = load_and_preprocess_data()

if df is None:
    st.error("Failed to load dataset. Please ensure 'player_injuries_impact.csv' is in the same directory.")
    st.stop()

# ============================================================================
# IMPROVED DASHBOARD HEADER
# ============================================================================
st.markdown('<div class="main-header">⚽ FOOTBALL INJURY IMPACT DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">🎯 Advanced Analytics for Team Performance Optimization | FootLens Analytics</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION & FILTERS
# ============================================================================
st.sidebar.header("🔍 FILTER & CUSTOMIZE")

with st.sidebar.expander("📋 Filter Options", expanded=True):
    selected_teams = st.multiselect(
        "🏆 Select Teams",
        options=sorted(df['Team Name'].unique()),
        default=sorted(df['Team Name'].unique()),
        key="teams_filter"
    )
    
    selected_seasons = st.multiselect(
        "📅 Select Seasons",
        options=sorted(df['Season'].unique()),
        default=sorted(df['Season'].unique()),
        key="seasons_filter"
    )
    
    selected_severity = st.multiselect(
        "🔴 Injury Severity",
        options=['Minor', 'Moderate', 'Severe'],
        default=['Minor', 'Moderate', 'Severe'],
        key="severity_filter"
    )
    
    selected_positions = st.multiselect(
        "👥 Player Position",
        options=sorted(df['Position'].unique()),
        default=sorted(df['Position'].unique()),
        key="position_filter"
    )
    
    age_groups = sorted(df['Age_Group'].dropna().unique())
    selected_age = st.multiselect(
        "👶 Age Group",
        options=age_groups,
        default=age_groups,
        key="age_filter"
    )

# Apply filters
df_filtered = df[
    (df['Team Name'].isin(selected_teams)) &
    (df['Season'].isin(selected_seasons)) &
    (df['Injury_Severity'].isin(selected_severity)) &
    (df['Position'].isin(selected_positions)) &
    (df['Age_Group'].isin(selected_age))
].copy()

# Sidebar Statistics
with st.sidebar.expander("📊 Quick Stats", expanded=True):
    st.metric("Total Records", len(df_filtered), f"({len(df)} overall)")
    st.metric("Unique Players", df_filtered['Name'].nunique(), f"({df['Name'].nunique()} total)")
    st.metric("Teams Analyzed", df_filtered['Team Name'].nunique(), f"({df['Team Name'].nunique()} total)")
    st.metric("Avg Injury Duration", f"{df_filtered['Injury_Duration_Days'].mean():.0f} days")

# ============================================================================
# KEY METRICS DASHBOARD (TOP ROW) - IMPROVED
# ============================================================================
st.markdown("---")
st.markdown("### 📈 KEY PERFORMANCE INDICATORS")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "Total Injuries",
        len(df_filtered),
        delta=f"{len(df) - len(df_filtered)} filtered",
        delta_color="off"
    )

with col2:
    avg_duration = df_filtered['Injury_Duration_Days'].mean()
    std_duration = df_filtered['Injury_Duration_Days'].std()
    st.metric(
        "Avg Recovery",
        f"{avg_duration:.0f} days",
        delta=f"±{std_duration:.1f}",
        delta_color="off"
    )

with col3:
    avg_perf_drop = df_filtered['Performance_Drop_Index'].mean()
    st.metric(
        "Performance Drop",
        f"{avg_perf_drop:.2f}",
        delta="Rating points",
        delta_color="inverse" if avg_perf_drop > 0 else "normal"
    )

with col4:
    most_common = df_filtered['Injury'].value_counts().index[0] if len(df_filtered) > 0 else "N/A"
    st.metric(
        "Most Common Injury",
        most_common[:15],
        delta=f"{df_filtered['Injury'].value_counts().values[0]} cases" if len(df_filtered) > 0 else "N/A",
        delta_color="off"
    )

with col5:
    team_perf_drop = df_filtered['Team_Performance_Drop'].mean()
    st.metric(
        "Team Perf Drop",
        f"{team_perf_drop:.2f}",
        delta="Goal Diff",
        delta_color="inverse" if team_perf_drop > 0 else "normal"
    )

with col6:
    win_drop = (df_filtered['Win_Ratio_Before'].mean() - df_filtered['Win_Ratio_During'].mean())
    st.metric(
        "Win Rate Drop",
        f"{win_drop:.1f}",
        delta="matches",
        delta_color="inverse" if win_drop > 0 else "normal"
    )

st.markdown("---")

# ============================================================================
# MULTI-TAB DASHBOARD
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview & Insights",
    "🔴 Injury Analysis",
    "👥 Player Performance",
    "🏆 Team Analytics",
    "📅 Temporal Patterns",
    "🔬 Advanced Statistics",
    "📋 Data Export"
])

# ========== TAB 1: OVERVIEW & INSIGHTS - IMPROVED DESIGN ==========
with tab1:
    st.markdown('<div class="tab-header">📊 RESEARCH INSIGHTS & KEY FINDINGS</div>', unsafe_allow_html=True)
    
    # RESEARCH QUESTION 1
    st.markdown('<div class="question-box">❓ Q1: Which injuries caused biggest performance drop?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_injuries = df_filtered.groupby('Injury').agg({
            'Team_Performance_Drop': 'mean',
            'Injury_Duration_Days': 'mean',
            'Name': 'count'
        }).sort_values('Team_Performance_Drop', ascending=False).head(3)
        
        for idx, (injury, row) in enumerate(top_injuries.iterrows(), 1):
            st.markdown(f"""
            <div class="insight-box">
            <strong>🥇 #{idx}: {injury}</strong><br>
            🔻 Avg Team Drop: <span class="stat-highlight">{row['Team_Performance_Drop']:.2f}</span> GD<br>
            ⏱️ Recovery: {row['Injury_Duration_Days']:.0f} days | 📊 Cases: {int(row['Name'])}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Top Performance Impact Metrics**")
        st.info(f"""
        ✅ **Highest Impact Injury**: {top_injuries.index[0]} ({top_injuries.iloc[0]['Team_Performance_Drop']:.2f} GD drop)
        
        📊 **Average Performance Drop**: {top_injuries['Team_Performance_Drop'].mean():.2f} Goal Difference
        
        ⏱️ **Average Recovery Time**: {top_injuries['Injury_Duration_Days'].mean():.0f} days
        
        📈 **Total Cases**: {int(top_injuries['Name'].sum())} injuries analyzed
        """)
    
    st.markdown("---")
    
    # RESEARCH QUESTION 2
    st.markdown('<div class="question-box">❓ Q2: Win/Loss record during player absence?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_win_before = df_filtered['Win_Ratio_Before'].sum()
        total_win_during = df_filtered['Win_Ratio_During'].sum()
        total_matches = len(df_filtered) * 3
        
        win_rate_before = (total_win_before / total_matches) * 100
        win_rate_during = (total_win_during / total_matches) * 100
        win_decrease = win_rate_before - win_rate_during
        
        st.markdown("""
        <div class="insight-box">
        <strong>Match Results Analysis</strong><br>
        ✅ <span class="stat-highlight">Before Injury: {:.1f}%</span> win rate<br>
        ❌ <span class="stat-highlight">During Absence: {:.1f}%</span> win rate<br>
        📉 <span class="stat-highlight">Decrease: {:.1f}%</span>
        </div>
        """.format(win_rate_before, win_rate_during, win_decrease), unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Win/Loss Summary**")
        st.success(f"✅ Total Wins Before: {int(total_win_before)} matches")
        st.error(f"❌ Total Wins During Absence: {int(total_win_during)} matches")
        st.warning(f"📉 Win Rate Drop: {win_decrease:.1f}%")
        st.info(f"📊 Total Matches Analyzed: {int(total_matches)}")
    
    st.markdown("---")
    
    # RESEARCH QUESTION 3
    st.markdown('<div class="question-box">❓ Q3: How did players perform after recovery?</div>', unsafe_allow_html=True)
    
    comeback_players = df_filtered[df_filtered['Performance_Drop_Index'].notna()].nlargest(5, 'Performance_Drop_Index')[
        ['Name', 'Team Name', 'Injury', 'Performance_Drop_Index', 'Injury_Duration_Days', 'Age']
    ]

    if len(comeback_players) > 0:
    rows = [comeback_players[0:3], comeback_players[3:5]]
    for row in rows:
        cols = st.columns(len(row))
        for idx, (_, r) in enumerate(row.iterrows()):
            with cols[idx]:
                st.markdown(f"""
                <div class="answer-box">
                <b>{r['Name']}</b><br>
                {r['Team Name']}<br>
                {r['Injury']}<br>
                <span class="stat-highlight">{r['Performance_Drop_Index']:.2f}</span> improvement points<br>
                {int(r['Injury_Duration_Days'])} days recovery
                </div>
                """, unsafe_allow_html=True)

    
    st.markdown("---")
    
    # RESEARCH QUESTION 4 & 5 - IMPROVED LAYOUT
    st.markdown('<div class="question-box">❓ Q4 & Q5: Injury clusters & most affected clubs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Monthly Injury Distribution")
        monthly_data = df_filtered['Injury_Month_Name'].value_counts().reindex(
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        )
        
        # Create a more readable format
        month_text = ""
        for month, count in monthly_data.items():
            if pd.notna(count) and count > 0:
                month_text += f"📅 {month}: {int(count)} injuries\n"
        
        st.success(month_text if month_text else "No data available")
    
    with col2:
        st.markdown("#### 🏆 Most Affected Clubs")
        club_injuries = df_filtered.groupby('Team Name').agg({
            'Name': 'count',
            'Team_Impact_Severity': 'mean'
        }).sort_values('Name', ascending=False).head(5)
        
        club_text = ""
        for idx, (team, row) in enumerate(club_injuries.iterrows(), 1):
            club_text += f"#{idx}. {team}: {int(row['Name'])} cases (Severity: {row['Team_Impact_Severity']:.2f})\n"
        
        st.info(club_text)

# ========== TAB 2: INJURY ANALYSIS ==========
with tab2:
    st.markdown('<div class="tab-header">🔴 COMPREHENSIVE INJURY IMPACT ANALYSIS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Injuries - Team Performance Impact")
        top_injuries_impact = df_filtered.groupby('Injury').agg({
            'Team_Performance_Drop': 'mean',
            'Name': 'count'
        }).sort_values('Team_Performance_Drop', ascending=False).head(10)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=top_injuries_impact.index,
            y=top_injuries_impact['Team_Performance_Drop'],
            marker=dict(
                color=top_injuries_impact['Team_Performance_Drop'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Performance Drop")
            ),
            text=top_injuries_impact['Team_Performance_Drop'].round(2),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg Drop: %{y:.2f} GD<extra></extra>',
            name='Performance Drop'
        ))
        fig1.update_layout(
            title="Top 10 Injuries by Team Performance Impact",
            xaxis_title="Injury Type",
            yaxis_title="Average Goal Difference Drop",
            height=480,
            template="plotly_white",
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Injury Severity Distribution")
        severity_dist = df_filtered['Injury_Severity'].value_counts()
        
        colors_map = {'Severe': DANGER_COLOR, 'Moderate': WARNING_COLOR, 'Minor': SUCCESS_COLOR}
        fig2 = go.Figure(data=[go.Pie(
            labels=severity_dist.index,
            values=severity_dist.values,
            hole=0.35,
            marker=dict(colors=[colors_map.get(x, '#999') for x in severity_dist.index]),
            textinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        fig2.update_layout(
            title="Distribution of Injury Severity Levels",
            height=480,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("#### Recovery Duration vs Performance Drop")
    
    fig3 = px.scatter(
        df_filtered[df_filtered['Performance_Drop_Index'].notna()],
        x='Injury_Duration_Days',
        y='Performance_Drop_Index',
        color='Injury_Severity',
        size='Team_Impact_Severity',
        hover_data=['Name', 'Team Name', 'Injury', 'Position', 'Age'],
        title='Injury Recovery Time vs Player Performance Drop',
        labels={
            'Injury_Duration_Days': 'Recovery Time (Days)',
            'Performance_Drop_Index': 'Performance Drop Index'
        },
        color_discrete_map={'Minor': SUCCESS_COLOR, 'Moderate': WARNING_COLOR, 'Severe': DANGER_COLOR},
        template="plotly_white"
    )
    fig3.update_layout(height=480)
    st.plotly_chart(fig3, use_container_width=True)

# ========== TAB 3: PLAYER PERFORMANCE ==========
with tab3:
    st.markdown('<div class="tab-header">👥 INDIVIDUAL PLAYER PERFORMANCE ANALYSIS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Most Injured Players (Top 15)")
        most_injured = df_filtered['Name'].value_counts().head(15)
        
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            y=most_injured.index,
            x=most_injured.values,
            orientation='h',
            marker=dict(color=most_injured.values, colorscale='Blues_r', showscale=True),
            text=most_injured.values,
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Injuries: %{x}<extra></extra>'
        ))
        fig5.update_layout(
            title="Players with Highest Injury Frequency",
            xaxis_title="Number of Injuries",
            height=500,
            template="plotly_white"
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.markdown("#### Comeback Players - Performance Improvement")
        comeback_data = df_filtered[df_filtered['Performance_Drop_Index'].notna()].nlargest(10, 'Performance_Drop_Index')[
            ['Name', 'Performance_Drop_Index', 'Injury', 'Injury_Duration_Days']
        ]
        
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(
            x=comeback_data['Name'],
            y=comeback_data['Performance_Drop_Index'],
            mode='markers+lines',
            marker=dict(
                size=12,
                color=comeback_data['Performance_Drop_Index'],
                colorscale='Greens',
                showscale=True,
                line=dict(width=2, color='white')
            ),
            text=comeback_data['Injury'],
            hovertemplate='<b>%{x}</b><br>Improvement: %{y:.2f} points<br>Injury: %{text}<extra></extra>',
            name='Improvement',
            line=dict(color=SUCCESS_COLOR, width=3)
        ))
        fig6.update_layout(
            title="Top Comeback Players (Performance Improvement)",
            xaxis_title="Player Name",
            yaxis_title="Performance Improvement Index",
            height=500,
            template="plotly_white",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🔍 Individual Player Deep Dive Analysis")
    
    selected_player = st.selectbox(
        "Select a player to analyze in detail:",
        options=sorted(df_filtered['Name'].unique()),
        key="player_selector"
    )
    
    player_data = df_filtered[df_filtered['Name'] == selected_player]
    
    if len(player_data) > 0:
        player_info = player_data.iloc[0]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Team", player_info['Team Name'])
        with col2:
            st.metric("Position", player_info['Position'])
        with col3:
            st.metric("Age", f"{player_info['Age']} years")
        with col4:
            st.metric("FIFA Rating", f"{player_info['FIFA rating']}")
        with col5:
            st.metric("Injuries", len(player_data))
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Rating Before", f"{player_info['Avg_Rating_Before_Injury']:.1f}" if not pd.isna(player_info['Avg_Rating_Before_Injury']) else "N/A")
        with col2:
            st.metric("Avg Rating After", f"{player_info['Avg_Rating_After_Injury']:.1f}" if not pd.isna(player_info['Avg_Rating_After_Injury']) else "N/A")
        with col3:
            st.metric("Recovery Time", f"{player_info['Injury_Duration_Days']:.0f} days")
        with col4:
            st.metric("Severity", player_info['Injury_Severity'])
        
        st.markdown("**Injury History:**")
        injury_history = player_data[['Date of Injury', 'Injury', 'Injury_Severity', 'Injury_Duration_Days', 'Performance_Drop_Index']].copy()
        injury_history['Date of Injury'] = injury_history['Date of Injury'].dt.strftime('%Y-%m-%d')
        st.dataframe(injury_history, use_container_width=True)

# ========== TAB 4: TEAM ANALYTICS ==========
with tab4:
    st.markdown('<div class="tab-header">🏆 TEAM-LEVEL PERFORMANCE ANALYSIS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Teams by Injury Frequency")
        team_injuries = df_filtered.groupby('Team Name').size().sort_values(ascending=False).head(10)
        
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            x=team_injuries.index,
            y=team_injuries.values,
            marker=dict(color=team_injuries.values, colorscale='Viridis', showscale=True),
            text=team_injuries.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>'
        ))
        fig7.update_layout(
            title="Top 10 Teams by Total Injury Cases",
            xaxis_title="Team",
            yaxis_title="Number of Injuries",
            height=450,
            template="plotly_white",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        st.markdown("#### Team Performance Drop by Club")
        team_perf = df_filtered.groupby('Team Name')['Team_Performance_Drop'].mean().sort_values(ascending=False).head(10)
        
        fig8 = go.Figure()
        fig8.add_trace(go.Bar(
            x=team_perf.index,
            y=team_perf.values,
            marker=dict(color=team_perf.values, colorscale='RdYlGn_r', showscale=True),
            text=team_perf.values.round(2),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg Drop: %{y:.2f} GD<extra></extra>'
        ))
        fig8.update_layout(
            title="Teams Most Affected by Injuries",
            xaxis_title="Team",
            yaxis_title="Average Performance Drop (GD)",
            height=450,
            template="plotly_white",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    st.markdown("#### 🔥 Injury Hotmap: Months vs Top 10 Clubs")
    
    top_teams = df_filtered['Team Name'].value_counts().head(10).index
    heatmap_data = df_filtered[df_filtered['Team Name'].isin(top_teams)].pivot_table(
        values='Name',
        index='Team Name',
        columns='Injury_Month_Name',
        aggfunc='count',
        fill_value=0
    )
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    heatmap_data = heatmap_data[[m for m in month_order if m in heatmap_data.columns]]
    
    fig9 = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd',
        hovertemplate='<b>%{y}</b> - %{x}<br>Injuries: %{z}<extra></extra>'
    ))
    fig9.update_layout(
        title="Injury Frequency Heatmap: Months × Teams",
        xaxis_title="Month",
        yaxis_title="Team",
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig9, use_container_width=True)

# ========== TAB 5: TEMPORAL PATTERNS ==========
with tab5:
    st.markdown('<div class="tab-header">📅 TEMPORAL TRENDS & SEASONAL PATTERNS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Injury Cases Across Seasons")
        season_injuries = df_filtered['Season'].value_counts().sort_index()
        
        fig11 = go.Figure()
        fig11.add_trace(go.Scatter(
            x=season_injuries.index,
            y=season_injuries.values,
            mode='lines+markers',
            line=dict(color=PRIMARY_COLOR, width=4),
            marker=dict(size=12, color=PRIMARY_COLOR, line=dict(width=2, color='white')),
            fill='tozeroy',
            hovertemplate='<b>%{x}</b><br>Injuries: %{y}<extra></extra>'
        ))
        fig11.update_layout(
            title="Injury Trend Across Seasons",
            xaxis_title="Season",
            yaxis_title="Number of Injuries",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig11, use_container_width=True)
    
    with col2:
        st.markdown("#### Average Recovery by Season")
        recovery_by_season = df_filtered.groupby('Season')['Injury_Duration_Days'].mean()
        
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(
            x=recovery_by_season.index,
            y=recovery_by_season.values,
            marker=dict(color=recovery_by_season.values, colorscale='Oranges', showscale=True),
            text=recovery_by_season.values.round(1),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg Recovery: %{y:.1f} days<extra></extra>'
        ))
        fig12.update_layout(
            title="Average Recovery Duration by Season",
            xaxis_title="Season",
            yaxis_title="Days",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig12, use_container_width=True)
    
    st.markdown("#### Monthly Injury Distribution")
    month_injuries = df_filtered['Injury_Month_Name'].value_counts().reindex(
        ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        fill_value=0
    )
    
    fig13 = go.Figure()
    fig13.add_trace(go.Bar(
        x=month_injuries.index,
        y=month_injuries.values,
        marker=dict(color=month_injuries.values, colorscale='Viridis', showscale=True),
        text=month_injuries.values,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Injuries: %{y}<extra></extra>'
    ))
    fig13.update_layout(
        title="Injury Distribution Across Months",
        xaxis_title="Month",
        yaxis_title="Number of Injuries",
        height=450,
        template="plotly_white",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig13, use_container_width=True)

# ========== TAB 6: ADVANCED STATISTICS ==========
with tab6:
    st.markdown('<div class="tab-header">🔬 ADVANCED STATISTICAL ANALYSIS</div>', unsafe_allow_html=True)
    
    st.markdown("#### Correlation Analysis")
    
    correlation_data = df_filtered[[
        'Age', 'FIFA rating', 'Injury_Duration_Days', 'Performance_Drop_Index',
        'Team_Performance_Drop', 'Win_Ratio_Before', 'Win_Ratio_During'
    ]].corr()
    
    fig15 = go.Figure(data=go.Heatmap(
        z=correlation_data.values,
        x=correlation_data.columns,
        y=correlation_data.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_data.values.round(2),
        texttemplate='%{text}',
        hovertemplate='%{y} vs %{x}: %{z:.3f}<extra></extra>'
    ))
    fig15.update_layout(
        title="Correlation Matrix: Key Variables",
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig15, use_container_width=True)
    
    st.markdown("#### Summary Statistics")
    summary_stats = df_filtered[[
        'Age', 'FIFA rating', 'Injury_Duration_Days', 'Performance_Drop_Index',
        'Team_Performance_Drop'
    ]].describe().round(2)
    st.dataframe(summary_stats, use_container_width=True)

# ========== TAB 7: DATA EXPORT ==========
with tab7:
    st.markdown('<div class="tab-header">📋 DATA EXPORT & DOWNLOAD</div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Filtered Dataset")
    
    columns_to_export = st.multiselect(
        "Select columns to export:",
        options=df_filtered.columns.tolist(),
        default=['Name', 'Team Name', 'Position', 'Age', 'Injury', 'Injury_Severity',
                'Injury_Duration_Days', 'Performance_Drop_Index', 'Team_Performance_Drop'],
        key="export_columns"
    )
    
    export_df = df_filtered[columns_to_export].sort_values('Performance_Drop_Index', ascending=False)
    
    st.dataframe(export_df, use_container_width=True, height=400)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"injury_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name='Injuries', index=False)
        excel_buffer.seek(0)
        st.download_button(
            label="📊 Download as Excel",
            data=excel_buffer,
            file_name=f"injury_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        json_data = export_df.to_json(orient='records', indent=2)
        st.download_button(
            label="🔗 Download as JSON",
            data=json_data,
            file_name=f"injury_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <strong>⚽ Football Injury Impact Dashboard v2.1 - Enhanced Design</strong><br>
    Developed for FootLens Analytics | Course: Mathematics for AI-II (IBDP)<br>
    Assignment: Developing User-Centered Dashboards to Solve Real-World Problems<br>
    <small>Data Source: Player Injuries & Team Performance | Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</small><br>
    <small>© 2025 FootLens Analytics. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)