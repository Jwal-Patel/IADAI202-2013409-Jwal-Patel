"""
⚽ FOOTBALL INJURY IMPACT DASHBOARD - CLEAN & MINIMALIST VERSION
========================================================
Professional, clean design with aesthetic appeal.
Focus on clarity and readability - NO excessive colors.

Company: FootLens Analytics
Role: Junior Sports Data Analyst
Course: Mathematics for AI-II (IBDP)

Author: AI Data Analytics Team
Version: 2.2 (Clean & Minimalist Design)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
from io import BytesIO

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Football Injury Impact Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CLEAN & MINIMALIST STYLING - Professional Look
# ============================================================================
st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Main Header - Clean and Simple */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1a1a1a;
        text-align: center;
        margin: 20px 0 10px 0;
        padding: 30px 20px;
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white;
        border-radius: 10px;
        letter-spacing: 1px;
    }
    
    /* Sub Header */
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #ecf0f1;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
    
    /* Tab Header - Minimalist */
    .tab-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 30px 0 20px 0;
        padding: 15px 0;
        border-bottom: 3px solid #3498db;
    }
    
    /* Question Box - CLEAN with visible text */
    .question-header {
        font-size: 1.4rem;
        font-weight: bold;
        color: white;
        background-color: #3498db;
        padding: 18px 20px;
        margin: 20px 0 15px 0;
        border-radius: 8px;
        border-left: 5px solid #2980b9;
    }
    
    /* Content Box with answer */
    .answer-box {
        background-color: #ecf0f1;
        border: 1px solid #bdc3c7;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
    
    /* Insight Box */
    .insight-box {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Metric Cards */
    .metric-label {
        color: #7f8c8d;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #7f8c8d;
        padding: 20px;
        font-size: 0.9rem;
        border-top: 2px solid #ecf0f1;
        margin-top: 40px;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Section title */
    .section-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #ecf0f1;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & PREPROCESSING
# ============================================================================
@st.cache_data
def load_and_preprocess_data():
    """Load and preprocess injury dataset."""
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
        
        missed_gd_cols = ['Match1_missed_match_GD', 'Match2_missed_match_GD', 'Match3_missed_match_GD']
        before_gd_cols = ['Match1_before_injury_GD', 'Match2_before_injury_GD', 'Match3_before_injury_GD']
        
        df['Avg_GD_Before'] = df[before_gd_cols].mean(axis=1)
        df['Team_Performance_During_Absence'] = df[missed_gd_cols].mean(axis=1)
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
    st.error("Failed to load dataset.")
    st.stop()

# ============================================================================
# DASHBOARD HEADER
# ============================================================================
st.markdown('<div class="main-header">⚽ FOOTBALL INJURY IMPACT DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Analytics for Team Performance Optimization | FootLens Analytics</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.header("Filter Options")

with st.sidebar.expander("Filters", expanded=True):
    selected_teams = st.multiselect("Select Teams", sorted(df['Team Name'].unique()), 
                                    default=sorted(df['Team Name'].unique()), key="teams")
    selected_seasons = st.multiselect("Select Seasons", sorted(df['Season'].unique()),
                                      default=sorted(df['Season'].unique()), key="seasons")
    selected_severity = st.multiselect("Injury Severity", ['Minor', 'Moderate', 'Severe'],
                                       default=['Minor', 'Moderate', 'Severe'], key="severity")
    selected_positions = st.multiselect("Player Position", sorted(df['Position'].unique()),
                                        default=sorted(df['Position'].unique()), key="positions")

# Apply filters
df_filtered = df[
    (df['Team Name'].isin(selected_teams)) &
    (df['Season'].isin(selected_seasons)) &
    (df['Injury_Severity'].isin(selected_severity)) &
    (df['Position'].isin(selected_positions))
].copy()

# Quick stats
with st.sidebar.expander("Statistics", expanded=True):
    st.metric("Total Injuries", len(df_filtered))
    st.metric("Unique Players", df_filtered['Name'].nunique())
    st.metric("Teams", df_filtered['Team Name'].nunique())
    st.metric("Avg Recovery", f"{df_filtered['Injury_Duration_Days'].mean():.0f} days")

# ============================================================================
# KEY METRICS
# ============================================================================
st.markdown("### Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Injuries", len(df_filtered))
with col2:
    st.metric("Avg Recovery", f"{df_filtered['Injury_Duration_Days'].mean():.0f} days")
with col3:
    st.metric("Performance Drop", f"{df_filtered['Performance_Drop_Index'].mean():.2f}")
with col4:
    st.metric("Most Common", df_filtered['Injury'].value_counts().index[0][:12] if len(df_filtered) > 0 else "N/A")
with col5:
    st.metric("Team Impact", f"{df_filtered['Team_Performance_Drop'].mean():.2f}")
with col6:
    st.metric("Win Drop", f"{(df_filtered['Win_Ratio_Before'].mean() - df_filtered['Win_Ratio_During'].mean()):.1f}")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Overview", "Injury Analysis", "Player Performance", "Team Analytics", "Temporal Patterns", "Statistics", "Data Export"
])

# ========== TAB 1: OVERVIEW ==========
with tab1:
    st.markdown('<div class="tab-header">Research Insights & Key Findings</div>', unsafe_allow_html=True)
    
    # Q1 - VISIBLE TEXT IN BOX
    st.markdown('<div class="question-header">❓ Q1: Which injuries caused biggest performance drop?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        top_injuries = df_filtered.groupby('Injury').agg({
            'Team_Performance_Drop': 'mean',
            'Injury_Duration_Days': 'mean',
            'Name': 'count'
        }).sort_values('Team_Performance_Drop', ascending=False).head(3)
        
        for idx, (injury, row) in enumerate(top_injuries.iterrows(), 1):
            st.markdown(f"""
            <div class="answer-box">
            <strong>#{idx}. {injury}</strong><br>
            Team Performance Drop: <strong>{row['Team_Performance_Drop']:.2f}</strong> GD<br>
            Recovery Time: <strong>{row['Injury_Duration_Days']:.0f}</strong> days | Cases: <strong>{int(row['Name'])}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-title" style="margin-top: 0;">Impact Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="insight-box">
        <strong>Highest Impact:</strong> {top_injuries.index[0]}<br>
        <strong>Drop:</strong> {top_injuries.iloc[0]['Team_Performance_Drop']:.2f} GD<br>
        <strong>Avg Recovery:</strong> {top_injuries['Injury_Duration_Days'].mean():.0f} days
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Q2 - VISIBLE TEXT IN BOX
    st.markdown('<div class="question-header">❓ Q2: Win/Loss record during player absence?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_win_before = df_filtered['Win_Ratio_Before'].sum()
        total_matches = len(df_filtered) * 3
        win_rate_before = (total_win_before / total_matches) * 100
        
        st.markdown(f"""
        <div class="answer-box">
        <strong>Win Rate Analysis</strong><br>
        Before Injury: <strong>{win_rate_before:.1f}%</strong><br>
        Wins: <strong>{int(total_win_before)}</strong> out of <strong>{int(total_matches)}</strong> matches
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_win_during = df_filtered['Win_Ratio_During'].sum()
        win_rate_during = (total_win_during / total_matches) * 100
        win_drop = win_rate_before - win_rate_during
        
        st.markdown(f"""
        <div class="answer-box">
        <strong>During Absence</strong><br>
        Win Rate: <strong>{win_rate_during:.1f}%</strong><br>
        Drop: <strong>{win_drop:.1f}%</strong> | Wins: <strong>{int(total_win_during)}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Q3 - VISIBLE TEXT IN BOX
    st.markdown('<div class="question-header">❓ Q3: How did players perform after recovery?</div>', unsafe_allow_html=True)
    
    comeback_players = df_filtered[df_filtered['Performance_Drop_Index'].notna()].nlargest(3, 'Performance_Drop_Index')[
        ['Name', 'Team Name', 'Injury', 'Performance_Drop_Index', 'Injury_Duration_Days']
    ]
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (i, (_, row)) in enumerate(zip([col1, col2, col3], comeback_players.iterrows())):
        with i:
            st.markdown(f"""
            <div class="answer-box">
            <strong>{row['Name']}</strong><br>
            Team: {row['Team Name']}<br>
            Injury: {row['Injury']}<br>
            Performance Improvement: <strong>{row['Performance_Drop_Index']:.2f}</strong> points<br>
            Recovery: <strong>{row['Injury_Duration_Days']:.0f}</strong> days
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Q4 & Q5
    st.markdown('<div class="question-header">❓ Q4 & Q5: Injury clusters & affected clubs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Monthly Distribution**")
        monthly_data = df_filtered['Injury_Month_Name'].value_counts().reindex(
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        )
        
        month_text = ""
        for month, count in monthly_data.items():
            if pd.notna(count) and count > 0:
                month_text += f"📅 {month}: {int(count)} injuries\n"
        
        st.markdown(f"""
        <div class="answer-box">
        {month_text}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Most Affected Clubs**")
        club_injuries = df_filtered.groupby('Team Name').size().sort_values(ascending=False).head(5)
        
        club_text = ""
        for idx, (team, count) in enumerate(club_injuries.items(), 1):
            club_text += f"#{idx}. {team}: {int(count)} cases\n"
        
        st.markdown(f"""
        <div class="answer-box">
        {club_text}
        </div>
        """, unsafe_allow_html=True)

# ========== TAB 2: INJURY ANALYSIS ==========
with tab2:
    st.markdown('<div class="tab-header">Injury Impact Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_injuries_impact = df_filtered.groupby('Injury')['Team_Performance_Drop'].mean().sort_values(ascending=False).head(10)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=top_injuries_impact.values,
            y=top_injuries_impact.index,
            orientation='h',
            marker=dict(color='#3498db', line=dict(color='#2980b9', width=1)),
            text=top_injuries_impact.values.round(2),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Drop: %{x:.2f}<extra></extra>'
        ))
        fig1.update_layout(
            title="Top Injuries by Team Impact",
            xaxis_title="Performance Drop",
            height=450,
            template="plotly_white",
            margin=dict(l=150)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        severity_dist = df_filtered['Injury_Severity'].value_counts()
        
        fig2 = go.Figure(data=[go.Pie(
            labels=severity_dist.index,
            values=severity_dist.values,
            marker=dict(colors=['#27ae60', '#f39c12', '#e74c3c']),
            textinfo='label+value',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
        )])
        fig2.update_layout(
            title="Injury Severity Distribution",
            height=450,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ========== TAB 3: PLAYER PERFORMANCE ==========
with tab3:
    st.markdown('<div class="tab-header">Player Performance Analysis</div>', unsafe_have_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        most_injured = df_filtered['Name'].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=most_injured.index,
            x=most_injured.values,
            orientation='h',
            marker=dict(color='#3498db'),
            text=most_injured.values,
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Injuries: %{x}<extra></extra>'
        ))
        fig.update_layout(
            title="Most Injured Players",
            xaxis_title="Number of Injuries",
            height=450,
            template="plotly_white",
            margin=dict(l=100)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        comeback = df_filtered[df_filtered['Performance_Drop_Index'].notna()].nlargest(10, 'Performance_Drop_Index')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=comeback['Name'],
            x=comeback['Performance_Drop_Index'],
            orientation='h',
            marker=dict(color='#27ae60'),
            text=comeback['Performance_Drop_Index'].round(2),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Improvement: %{x:.2f}<extra></extra>'
        ))
        fig.update_layout(
            title="Top Comeback Players",
            xaxis_title="Performance Improvement",
            height=450,
            template="plotly_white",
            margin=dict(l=150)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Select Player for Details**")
    selected_player = st.selectbox("Player", options=sorted(df_filtered['Name'].unique()))
    
    player_info = df_filtered[df_filtered['Name'] == selected_player].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Team", player_info['Team Name'])
    with col2:
        st.metric("Position", player_info['Position'])
    with col3:
        st.metric("Age", player_info['Age'])
    with col4:
        st.metric("FIFA Rating", player_info['FIFA rating'])

# ========== TAB 4: TEAM ANALYTICS ==========
with tab4:
    st.markdown('<div class="tab-header">Team Performance Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        team_injuries = df_filtered.groupby('Team Name').size().sort_values(ascending=False).head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=team_injuries.index,
            y=team_injuries.values,
            marker=dict(color='#3498db'),
            text=team_injuries.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>'
        ))
        fig.update_layout(
            title="Teams by Injury Frequency",
            yaxis_title="Number of Cases",
            height=450,
            template="plotly_white",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        team_perf = df_filtered.groupby('Team Name')['Team_Performance_Drop'].mean().sort_values(ascending=False).head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=team_perf.index,
            y=team_perf.values,
            marker=dict(color='#e74c3c'),
            text=team_perf.values.round(2),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Drop: %{y:.2f}<extra></extra>'
        ))
        fig.update_layout(
            title="Teams Most Affected",
            yaxis_title="Avg Performance Drop",
            height=450,
            template="plotly_white",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

# ========== TAB 5: TEMPORAL PATTERNS ==========
with tab5:
    st.markdown('<div class="tab-header">Temporal Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        season_injuries = df_filtered['Season'].value_counts().sort_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=season_injuries.index,
            y=season_injuries.values,
            mode='lines+markers',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>'
        ))
        fig.update_layout(
            title="Injuries Across Seasons",
            yaxis_title="Count",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        recovery_season = df_filtered.groupby('Season')['Injury_Duration_Days'].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=recovery_season.index,
            y=recovery_season.values,
            marker=dict(color='#f39c12'),
            text=recovery_season.values.round(1),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Days: %{y:.1f}<extra></extra>'
        ))
        fig.update_layout(
            title="Avg Recovery by Season",
            yaxis_title="Days",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

# ========== TAB 6: STATISTICS ==========
with tab6:
    st.markdown('<div class="tab-header">Statistical Analysis</div>', unsafe_allow_html=True)
    
    corr_data = df_filtered[['Age', 'FIFA rating', 'Injury_Duration_Days', 'Performance_Drop_Index', 'Team_Performance_Drop']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_data.values,
        x=corr_data.columns,
        y=corr_data.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_data.values.round(2),
        texttemplate='%{text}'
    ))
    fig.update_layout(title="Correlation Matrix", height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Summary Statistics**")
    summary = df_filtered[['Age', 'Injury_Duration_Days', 'Performance_Drop_Index', 'Team_Performance_Drop']].describe()
    st.dataframe(summary, use_container_width=True)

# ========== TAB 7: DATA EXPORT ==========
with tab7:
    st.markdown('<div class="tab-header">Data Export</div>', unsafe_allow_html=True)
    
    cols = st.multiselect(
        "Select columns to export",
        options=df_filtered.columns.tolist(),
        default=['Name', 'Team Name', 'Injury', 'Injury_Duration_Days', 'Performance_Drop_Index']
    )
    
    export_df = df_filtered[cols]
    st.dataframe(export_df, use_container_width=True, height=400)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = export_df.to_csv(index=False)
        st.download_button("📥 CSV", csv, f"data_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with col2:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as w:
            export_df.to_excel(w, index=False)
        buffer.seek(0)
        st.download_button("📊 Excel", buffer, f"data_{datetime.now().strftime('%Y%m%d')}.xlsx", 
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    with col3:
        json = export_df.to_json(orient='records')
        st.download_button("🔗 JSON", json, f"data_{datetime.now().strftime('%Y%m%d')}.json", "application/json")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <strong>Football Injury Impact Dashboard v2.2</strong><br>
    Developed for FootLens Analytics | Mathematics for AI-II (IBDP)<br>
    Data Source: Player Injuries & Team Performance | Updated: {datetime.now().strftime('%B %d, %Y')}<br>
    © 2025 FootLens Analytics. All rights reserved.
</div>
""", unsafe_allow_html=True)