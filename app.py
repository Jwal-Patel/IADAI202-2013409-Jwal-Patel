"""
⚽ FOOTBALL INJURY IMPACT DASHBOARD - MINIMALIST ELEGANT VERSION
========================================================
A clean, professional Streamlit dashboard with minimalist design.
Focuses on elegance, simplicity, and clear visibility.

Company: FootLens Analytics
Course: Mathematics for AI-II (IBDP)
Version: 3.0 (Minimalist Elegant Design)
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
# MINIMALIST STYLING - CLEAN & ELEGANT
# ============================================================================
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Main title - Simple and elegant */
    .main-header {
        font-size: 2.8rem;
        font-weight: 600;
        color: #1a1a1a;
        margin: 30px 0 10px 0;
        padding: 20px 0;
        letter-spacing: 0.5px;
    }
    
    /* Subtitle - Minimalist */
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 30px;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* Question boxes - Clean with light blue background */
    .question-box {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a3a52;
        background-color: #e8f1f8;
        padding: 18px 20px;
        margin: 25px 0;
        border-radius: 8px;
        border-left: 4px solid #2c5aa0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Insight boxes - Elegant and minimal */
    .insight-box {
        background-color: #f5f8fc;
        padding: 16px 18px;
        border-radius: 6px;
        border-left: 3px solid #2c5aa0;
        margin: 12px 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Tab header - Clean */
    .tab-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin: 25px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* Stats highlight - Minimal */
    .stat-highlight {
        background-color: #e8f1f8;
        color: #2c5aa0;
        padding: 8px 12px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        margin: 4px 4px 4px 0;
    }
    
    /* Footer - Simple and clean */
    .footer {
        text-align: center;
        color: #999;
        padding: 20px;
        font-size: 0.85rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 40px;
        background-color: #f8f9fa;
    }
    
    /* Metric cards - Minimal styling */
    .metric-card {
        background-color: white;
        padding: 16px;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & PREPROCESSING
# ============================================================================
@st.cache_data
def load_and_preprocess_data():
    """Load and preprocess the injury dataset."""
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
        
        df['Performance_Category'] = pd.cut(df['FIFA rating'], 
                                           bins=[0, 75, 80, 85, 100],
                                           labels=['Average', 'Good', 'Very Good', 'Elite'])
        
        # Handle missing values
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
# DASHBOARD HEADER - MINIMALIST
# ============================================================================
st.markdown('<div class="main-header">⚽ Football Injury Impact Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Analytics for Team Performance | FootLens Analytics</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.header("Filters")

with st.sidebar.expander("Filter Options", expanded=True):
    selected_teams = st.multiselect(
        "Teams",
        options=sorted(df['Team Name'].unique()),
        default=sorted(df['Team Name'].unique())
    )
    
    selected_seasons = st.multiselect(
        "Seasons",
        options=sorted(df['Season'].unique()),
        default=sorted(df['Season'].unique())
    )
    
    selected_severity = st.multiselect(
        "Injury Severity",
        options=['Minor', 'Moderate', 'Severe'],
        default=['Minor', 'Moderate', 'Severe']
    )
    
    selected_positions = st.multiselect(
        "Position",
        options=sorted(df['Position'].unique()),
        default=sorted(df['Position'].unique())
    )
    
    age_groups = sorted(df['Age_Group'].dropna().unique())
    selected_age = st.multiselect(
        "Age Group",
        options=age_groups,
        default=age_groups
    )

# Apply filters
df_filtered = df[
    (df['Team Name'].isin(selected_teams)) &
    (df['Season'].isin(selected_seasons)) &
    (df['Injury_Severity'].isin(selected_severity)) &
    (df['Position'].isin(selected_positions)) &
    (df['Age_Group'].isin(selected_age))
].copy()

# ============================================================================
# KEY METRICS - SIMPLE
# ============================================================================
st.markdown("---")
st.markdown("**Key Metrics**")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Injuries", len(df_filtered))
with col2:
    st.metric("Avg Recovery", f"{df_filtered['Injury_Duration_Days'].mean():.0f} days")
with col3:
    st.metric("Performance Drop", f"{df_filtered['Performance_Drop_Index'].mean():.2f}")
with col4:
    st.metric("Unique Players", df_filtered['Name'].nunique())
with col5:
    st.metric("Teams", df_filtered['Team Name'].nunique())
with col6:
    st.metric("Most Common", df_filtered['Injury'].mode()[0][:15] if len(df_filtered) > 0 else "N/A")

st.markdown("---")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Overview", 
    "Injuries", 
    "Players", 
    "Teams", 
    "Trends",
    "Statistics",
    "Export"
])

# ========== TAB 1: OVERVIEW ==========
with tab1:
    st.markdown('<div class="tab-header">Research Insights & Findings</div>', unsafe_allow_html=True)
    
    # Q1 - Visible text in blue box
    st.markdown('<div class="question-box">Q1: Which injuries caused biggest performance drop?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        top_injuries = df_filtered.groupby('Injury').agg({
            'Team_Performance_Drop': 'mean',
            'Name': 'count'
        }).sort_values('Team_Performance_Drop', ascending=False).head(3)
        
        for idx, (injury, row) in enumerate(top_injuries.iterrows(), 1):
            st.markdown(f"""
            <div class="insight-box">
            <strong>#{idx} {injury}</strong><br>
            Performance Drop: <span class="stat-highlight">{row['Team_Performance_Drop']:.2f} GD</span><br>
            Cases: {int(row['Name'])}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.info(f"""
        **Insight**
        
        Highest Impact: {top_injuries.index[0]}
        
        Avg Drop: {top_injuries['Team_Performance_Drop'].mean():.2f} GD
        """)
    
    st.markdown("")
    
    # Q2
    st.markdown('<div class="question-box">Q2: Win/Loss record during player absence?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        total_win_before = df_filtered['Win_Ratio_Before'].sum()
        total_win_during = df_filtered['Win_Ratio_During'].sum()
        total_matches = len(df_filtered) * 3
        
        win_rate_before = (total_win_before / total_matches) * 100
        win_rate_during = (total_win_during / total_matches) * 100
        
        st.markdown(f"""
        <div class="insight-box">
        <strong>Match Performance Analysis</strong><br>
        Before Injury: <span class="stat-highlight">{win_rate_before:.1f}%</span> wins<br>
        During Absence: <span class="stat-highlight">{win_rate_during:.1f}%</span> wins<br>
        Drop: {win_rate_before - win_rate_during:.1f}%
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.success(f"""
        **Summary**
        
        Wins Before: {int(total_win_before)}
        
        Wins During: {int(total_win_during)}
        """)
    
    st.markdown("")
    
    # Q3
    st.markdown('<div class="question-box">Q3: How did players perform after recovery?</div>', unsafe_allow_html=True)
    
    comeback_players = df_filtered[df_filtered['Performance_Drop_Index'].notna()].nlargest(3, 'Performance_Drop_Index')[
        ['Name', 'Team Name', 'Injury', 'Performance_Drop_Index']
    ]
    
    cols = st.columns(3)
    for idx, (_, row) in enumerate(comeback_players.iterrows()):
        with cols[idx]:
            st.markdown(f"""
            <div class="insight-box">
            <strong>{row['Name']}</strong><br>
            {row['Team Name']}<br>
            Injury: {row['Injury']}<br>
            Improvement: <span class="stat-highlight">{row['Performance_Drop_Index']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Q4 & Q5
    st.markdown('<div class="question-box">Q4 & Q5: Injury clusters & most affected clubs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Monthly Distribution**")
        monthly_data = df_filtered['Injury_Month_Name'].value_counts().reindex(
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        )
        
        month_text = ""
        for month, count in monthly_data.items():
            if pd.notna(count) and count > 0:
                month_text += f"• {month}: {int(count)}\n"
        
        st.code(month_text, language=None)
    
    with col2:
        st.markdown("**Top Affected Clubs**")
        club_injuries = df_filtered.groupby('Team Name').size().sort_values(ascending=False).head(5)
        
        club_text = ""
        for idx, (team, count) in enumerate(club_injuries.items(), 1):
            club_text += f"{idx}. {team}: {count}\n"
        
        st.code(club_text, language=None)

# ========== TAB 2: INJURIES ==========
with tab2:
    st.markdown('<div class="tab-header">Injury Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_injuries_impact = df_filtered.groupby('Injury')['Team_Performance_Drop'].mean().sort_values(ascending=False).head(8)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=top_injuries_impact.index,
            y=top_injuries_impact.values,
            marker=dict(color='#2c5aa0', opacity=0.7),
            text=top_injuries_impact.values.round(2),
            textposition='outside'
        ))
        fig1.update_layout(
            title="Top Injuries by Performance Impact",
            xaxis_title="Injury Type",
            yaxis_title="Avg Performance Drop",
            height=400,
            template="plotly_white",
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        severity_dist = df_filtered['Injury_Severity'].value_counts()
        
        fig2 = go.Figure(data=[go.Pie(
            labels=severity_dist.index,
            values=severity_dist.values,
            hole=0.3,
            marker=dict(colors=['#2c5aa0', '#5a8ac2', '#8ab0d9']),
            textinfo='label+percent'
        )])
        fig2.update_layout(
            title="Injury Severity Distribution",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ========== TAB 3: PLAYERS ==========
with tab3:
    st.markdown('<div class="tab-header">Player Performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        most_injured = df_filtered['Name'].value_counts().head(10)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=most_injured.index,
            x=most_injured.values,
            orientation='h',
            marker=dict(color='#2c5aa0', opacity=0.7),
            text=most_injured.values,
            textposition='outside'
        ))
        fig3.update_layout(
            title="Most Injured Players",
            xaxis_title="Number of Injuries",
            height=400,
            template="plotly_white",
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("**Individual Player Analysis**")
        selected_player = st.selectbox(
            "Select player:",
            options=sorted(df_filtered['Name'].unique()),
            key="player_selector"
        )
        
        player_data = df_filtered[df_filtered['Name'] == selected_player]
        if len(player_data) > 0:
            player_info = player_data.iloc[0]
            st.markdown(f"""
            **{player_info['Name']}**
            
            Team: {player_info['Team Name']}
            Position: {player_info['Position']}
            Age: {player_info['Age']}
            FIFA Rating: {player_info['FIFA rating']}
            
            Avg Rating Before: {player_info['Avg_Rating_Before_Injury']:.1f if not pd.isna(player_info['Avg_Rating_Before_Injury']) else 'N/A'}
            Avg Rating After: {player_info['Avg_Rating_After_Injury']:.1f if not pd.isna(player_info['Avg_Rating_After_Injury']) else 'N/A'}
            Recovery Time: {player_info['Injury_Duration_Days']:.0f} days
            """)

# ========== TAB 4: TEAMS ==========
with tab4:
    st.markdown('<div class="tab-header">Team Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        team_injuries = df_filtered.groupby('Team Name').size().sort_values(ascending=False).head(10)
        
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=team_injuries.index,
            y=team_injuries.values,
            marker=dict(color='#2c5aa0', opacity=0.7),
            text=team_injuries.values,
            textposition='outside'
        ))
        fig4.update_layout(
            title="Team Injury Frequency",
            xaxis_title="Team",
            yaxis_title="Number of Injuries",
            height=400,
            template="plotly_white",
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        team_perf = df_filtered.groupby('Team Name')['Team_Performance_Drop'].mean().sort_values(ascending=False).head(10)
        
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=team_perf.index,
            y=team_perf.values,
            marker=dict(color='#5a8ac2', opacity=0.7),
            text=team_perf.values.round(2),
            textposition='outside'
        ))
        fig5.update_layout(
            title="Team Performance Impact",
            xaxis_title="Team",
            yaxis_title="Avg Performance Drop",
            height=400,
            template="plotly_white",
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig5, use_container_width=True)

# ========== TAB 5: TRENDS ==========
with tab5:
    st.markdown('<div class="tab-header">Temporal Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        season_injuries = df_filtered['Season'].value_counts().sort_index()
        
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(
            x=season_injuries.index,
            y=season_injuries.values,
            mode='lines+markers',
            line=dict(color='#2c5aa0', width=2),
            marker=dict(size=8),
            fill='tozeroy'
        ))
        fig6.update_layout(
            title="Injuries by Season",
            xaxis_title="Season",
            yaxis_title="Count",
            height=400,
            template="plotly_white",
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        month_injuries = df_filtered['Injury_Month_Name'].value_counts().reindex(
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            fill_value=0
        )
        
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            x=month_injuries.index,
            y=month_injuries.values,
            marker=dict(color='#2c5aa0', opacity=0.7),
            text=month_injuries.values,
            textposition='outside'
        ))
        fig7.update_layout(
            title="Monthly Distribution",
            xaxis_title="Month",
            yaxis_title="Injuries",
            height=400,
            template="plotly_white",
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig7, use_container_width=True)

# ========== TAB 6: STATISTICS ==========
with tab6:
    st.markdown('<div class="tab-header">Statistical Analysis</div>', unsafe_allow_html=True)
    
    correlation_data = df_filtered[[
        'Age', 'FIFA rating', 'Injury_Duration_Days', 'Performance_Drop_Index',
        'Team_Performance_Drop'
    ]].corr()
    
    fig8 = go.Figure(data=go.Heatmap(
        z=correlation_data.values,
        x=correlation_data.columns,
        y=correlation_data.columns,
        colorscale='Blues',
        zmid=0,
        text=correlation_data.values.round(2),
        texttemplate='%{text}',
        hovertemplate='%{y} vs %{x}: %{z:.3f}<extra></extra>'
    ))
    fig8.update_layout(
        title="Correlation Matrix",
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig8, use_container_width=True)
    
    st.markdown("**Summary Statistics**")
    summary_stats = df_filtered[[
        'Age', 'FIFA rating', 'Injury_Duration_Days', 'Performance_Drop_Index',
        'Team_Performance_Drop'
    ]].describe().round(2)
    st.dataframe(summary_stats, use_container_width=True)

# ========== TAB 7: EXPORT ==========
with tab7:
    st.markdown('<div class="tab-header">Data Export</div>', unsafe_allow_html=True)
    
    columns_to_export = st.multiselect(
        "Select columns to export:",
        options=df_filtered.columns.tolist(),
        default=['Name', 'Team Name', 'Position', 'Age', 'Injury', 'Injury_Severity',
                'Injury_Duration_Days', 'Performance_Drop_Index']
    )
    
    export_df = df_filtered[columns_to_export].sort_values('Performance_Drop_Index', ascending=False)
    
    st.dataframe(export_df, use_container_width=True, height=400)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"injury_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name='Injuries', index=False)
        excel_buffer.seek(0)
        st.download_button(
            label="Download Excel",
            data=excel_buffer,
            file_name=f"injury_analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        json_data = export_df.to_json(orient='records', indent=2)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"injury_analysis_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# ============================================================================
# FOOTER - SIMPLE
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div class="footer">
⚽ Football Injury Impact Dashboard v3.0<br>
FootLens Analytics | Mathematics for AI-II (IBDP)<br>
Last Updated: {datetime.now().strftime('%B %d, %Y')}
</div>
""", unsafe_allow_html=True)