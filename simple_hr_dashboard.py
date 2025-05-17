import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide"
)

# Custom color palettes
# Primary color palette
PRIMARY_COLOR = "#4361EE"  # Main theme color (blue)
SECONDARY_COLOR = "#3A0CA3"  # Secondary color (darker blue/purple)
ACCENT_COLOR = "#7209B7"  # Accent color (purple)
HIGHLIGHT_COLOR = "#F72585"  # Highlight color (pink)

# Background colors
BG_COLOR = "#000000"  # Black background
CARD_BG_COLOR = "#121212"  # Dark gray for cards
SIDEBAR_BG_COLOR = "#000000"  # Sidebar background

# Text colors
TEXT_COLOR = "#F8FAFC"  # Light gray for text
MUTED_TEXT_COLOR = "#94A3B8"  # Muted text

# Department colors - assign a unique color to each department
DEPARTMENT_COLORS = {
    "Sales": "#4CC9F0",  # Light blue
    "IT": "#4361EE",     # Blue
    "R&D": "#3A0CA3",    # Purple
    "HR": "#7209B7",     # Violet
    "Finance": "#F72585", # Pink
    "Marketing": "#4895EF", # Sky blue
    "Operations": "#560BAD", # Dark purple
    "Customer Service": "#F77F00" # Orange
}

# Performance colors
PERFORMANCE_COLORS = {
    1: "#F94144",  # Red (Poor)
    2: "#F8961E",  # Orange (Below Average)
    3: "#F9C74F",  # Yellow (Average)
    4: "#90BE6D",  # Light green (Good)
    5: "#43AA8B"   # Green (Excellent)
}

# Gender colors
GENDER_COLORS = {
    "Male": "#4361EE",  # Blue
    "Female": "#F72585" # Pink
}

# Custom CSS to match the color scheme
st.markdown(f"""
<style>
    /* Page background */
    .main {{
        background-color: {BG_COLOR};
        padding-top: 0rem;
    }}
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 0rem;
    }}
    /* Text colors */
    h1, h2, h3, h4, h5, h6, p, div {{
        color: {TEXT_COLOR} !important;
    }}
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG_COLOR};
    }}
    /* Metric styling */
    .css-1xarl3l {{
        font-size: 1.8rem;
        color: {TEXT_COLOR};
    }}
    /* Card styling */
    .stCard {{
        background-color: {CARD_BG_COLOR};
        border-radius: 8px;
        padding: 10px;
    }}
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {CARD_BG_COLOR};
        color: {TEXT_COLOR};
        border-radius: 4px 4px 0 0;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {PRIMARY_COLOR} !important;
        color: white !important;
    }}
    /* Custom border for sections */
    .dashboard-section {{
        background-color: {CARD_BG_COLOR};
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }}
    /* Metric card */
    div[data-testid="metric-container"] {{
        background-color: {CARD_BG_COLOR};
        border-radius: 8px;
        padding: 10px;
        border-left: 5px solid {PRIMARY_COLOR};
    }}
    /* Links */
    a {{
        color: {PRIMARY_COLOR} !important;
    }}
    /* Buttons */
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    /* Progress bar */
    .stProgress>div>div>div>div {{
        background-color: {PRIMARY_COLOR};
    }}
</style>
""", unsafe_allow_html=True)

# Function to create styled section headers
def section_header(title):
    st.markdown(f"""
    <div style="background-color: {CARD_BG_COLOR}; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid {PRIMARY_COLOR};">
        <h3 style="margin-bottom: 0; color: {TEXT_COLOR};">{title}</h3>
    </div>
    """, unsafe_allow_html=True)

# Function to create styled card
def styled_card(title, content, icon=None):
    icon_html = f"<span style='font-size: 1.5rem; margin-right: 10px;'>{icon}</span>" if icon else ""
    
    st.markdown(f"""
    <div style="background-color: {CARD_BG_COLOR}; padding: 15px; border-radius: 8px; height: 100%; border-left: 5px solid {PRIMARY_COLOR};">
        <h4 style="margin-bottom: 5px; color: {MUTED_TEXT_COLOR};">{icon_html}{title}</h4>
        <h2 style="font-size: 2rem; margin: 0; color: {TEXT_COLOR};">{content}</h2>
    </div>
    """, unsafe_allow_html=True)

# Function to generate sample HR data
def create_sample_data(n_employees=200):
    np.random.seed(42)
    
    # Define departments and job roles
    departments = list(DEPARTMENT_COLORS.keys())
    job_roles = ['Manager', 'Senior', 'Junior', 'Intern']
    
    # Create employee data
    data = []
    
    for i in range(1, n_employees + 1):
        # Basic employee information
        employee = {
            'EmployeeID': i,
            'Age': np.random.randint(22, 60),
            'Gender': np.random.choice(['Male', 'Female']),
            'Department': np.random.choice(departments),
            'JobRole': np.random.choice(job_roles),
            'Salary': np.random.randint(30000, 120000),
            'YearsAtCompany': np.random.randint(0, 20),
            'JobSatisfaction': np.random.randint(1, 5),
            'PerformanceRating': np.random.randint(1, 6),  # 1-5 scale
            'WorkLifeBalance': np.random.randint(1, 5)
        }
        
        # Calculate attrition probability based on various factors
        attrition_prob = 0.15  # Base probability
        
        # Low satisfaction increases attrition
        attrition_prob += (5 - employee['JobSatisfaction']) * 0.05
        
        # Low salary increases attrition
        if employee['Salary'] < 50000:
            attrition_prob += 0.1
            
        # New employees more likely to leave
        if employee['YearsAtCompany'] < 2:
            attrition_prob += 0.1
            
        # Cap probability between 0.05 and 0.8
        attrition_prob = max(0.05, min(attrition_prob, 0.8))
        
        # Determine if employee left based on probability
        employee['Attrition'] = 'Yes' if np.random.random() < attrition_prob else 'No'
        
        # Add to dataset
        data.append(employee)
    
    return pd.DataFrame(data)

# Load data
df = create_sample_data()

# Dashboard title and header
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; background-color: {CARD_BG_COLOR}; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 5px solid {PRIMARY_COLOR};">
    <div>
        <h1 style="margin-bottom: 0; color: {TEXT_COLOR}; display: flex; align-items: center;">
            <span style="color: {PRIMARY_COLOR}; margin-right: 10px;">HR</span> Analytics Dashboard <span style="font-size: 1rem; margin-left: 10px; color: {MUTED_TEXT_COLOR};">| Overview</span>
        </h1>
    </div>
    <div>
        <button style="background-color: {PRIMARY_COLOR}; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer;">Filter</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for filtering
st.sidebar.title("Filters")

# Department filter
departments = sorted(df['Department'].unique())
department_filter = st.sidebar.multiselect(
    "Department",
    options=departments,
    default=departments
)

# Job Role filter
job_roles = sorted(df['JobRole'].unique())
job_role_filter = st.sidebar.multiselect(
    "Job Role",
    options=job_roles,
    default=job_roles
)

# Gender filter
genders = sorted(df['Gender'].unique())
gender_filter = st.sidebar.multiselect(
    "Gender",
    options=genders,
    default=genders
)

# Performance filter
performance_options = sorted(df['PerformanceRating'].unique())
performance_filter = st.sidebar.multiselect(
    "Performance Rating",
    options=performance_options,
    default=performance_options
)

# Apply filters
filtered_df = df[
    df['Department'].isin(department_filter) & 
    df['JobRole'].isin(job_role_filter) &
    df['Gender'].isin(gender_filter) &
    df['PerformanceRating'].isin(performance_filter)
]

# Display data summary
st.sidebar.markdown("---")
st.sidebar.subheader("Data Summary")
st.sidebar.write(f"Total Employees: {len(filtered_df)}")
st.sidebar.write(f"Departments: {len(filtered_df['Department'].unique())}")
st.sidebar.write(f"Job Roles: {len(filtered_df['JobRole'].unique())}")

# Create tabs for navigation
tab_names = ["Overview", "Demographics", "Performance", "Attrition", "Compensation"]
tabs = st.tabs(tab_names)

# Overview tab
with tabs[0]:
    # Top KPIs row
    st.subheader("Key Metrics")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    # Calculate key metrics
    total_employees = len(filtered_df)
    active_employees = filtered_df[filtered_df['Attrition'] == 'No'].shape[0]
    attrition_count = filtered_df[filtered_df['Attrition'] == 'Yes'].shape[0]
    attrition_rate = round((attrition_count / total_employees) * 100, 1) if total_employees > 0 else 0
    avg_performance = round(filtered_df['PerformanceRating'].mean(), 1)
    avg_satisfaction = round(filtered_df['JobSatisfaction'].mean(), 1)
    
    # Display KPIs
    with kpi_col1:
        styled_card("Total Employees", f"{total_employees:,}", "👥")
    
    with kpi_col2:
        styled_card("Active Employees", f"{active_employees:,}", "👤")
    
    with kpi_col3:
        styled_card("Attrition Rate", f"{attrition_rate}%", "🔄")
    
    with kpi_col4:
        styled_card("Avg Performance", f"{avg_performance}/5", "⭐")
    
    # Department distribution and demographics
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        section_header("Department Distribution")
        
        # Department horizontal bar chart
        dept_counts = filtered_df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Count']
        
        # Sort by count descending
        dept_counts = dept_counts.sort_values('Count', ascending=False)
        
        # Create colors list based on department
        colors = [DEPARTMENT_COLORS.get(dept, PRIMARY_COLOR) for dept in dept_counts['Department']]
        
        fig = px.bar(
            dept_counts,
            x='Count',
            y='Department',
            orientation='h',
            title='Employees by Department',
            text='Count',
            color='Department',
            color_discrete_map=DEPARTMENT_COLORS
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            yaxis_title='',
            xaxis_title='Number of Employees',
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_header("Gender Distribution")
        
        # Gender donut chart
        gender_counts = filtered_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        
        fig = px.pie(
            gender_counts,
            values='Count',
            names='Gender',
            title='Gender Breakdown',
            hole=0.6,
            color='Gender',
            color_discrete_map=GENDER_COLORS
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
            height=400
        )
        
        fig.update_traces(textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance by department
    st.markdown("---")
    section_header("Performance by Department")
    
    # Calculate average performance by department
    perf_by_dept = filtered_df.groupby('Department')['PerformanceRating'].mean().reset_index()
    perf_by_dept = perf_by_dept.sort_values('PerformanceRating', ascending=False)
    
    # Create a color scale based on performance
    fig = px.bar(
        perf_by_dept,
        x='Department',
        y='PerformanceRating',
        title='Average Performance Rating by Department',
        color='PerformanceRating',
        text=perf_by_dept['PerformanceRating'].round(1)
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        xaxis_title='',
        yaxis_title='Average Performance Rating (1-5)',
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary distribution
    st.markdown("---")
    section_header("Salary Distribution")
    
    # Salary boxplot by department
    fig = px.box(
        filtered_df,
        x='Department',
        y='Salary',
        color='Department',
        title='Salary Distribution by Department',
        color_discrete_map=DEPARTMENT_COLORS
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        xaxis_title='',
        yaxis_title='Salary ($)',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Job satisfaction vs performance
    st.markdown("---")
    section_header("Job Satisfaction vs Performance")
    
    # Create scatter plot with performance colors
    fig = px.scatter(
        filtered_df,
        x='JobSatisfaction',
        y='PerformanceRating',
        color='Department',
        size='YearsAtCompany',
        hover_data=['JobRole', 'Gender', 'Salary'],
        color_discrete_map=DEPARTMENT_COLORS,
        title='Relationship Between Job Satisfaction and Performance'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        xaxis_title='Job Satisfaction (1-4)',
        yaxis_title='Performance Rating (1-5)',
        legend=dict(
            title='Department',
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Demographics tab
with tabs[1]:
    st.subheader("Employee Demographics")
    
    # Age distribution
    col1, col2 = st.columns(2)
    
    with col1:
        section_header("Age Distribution")
        
        # Create age bins
        bins = [20, 30, 40, 50, 60, 70]
        labels = ['20-29', '30-39', '40-49', '50-59', '60+']
        filtered_df['AgeGroup'] = pd.cut(filtered_df['Age'], bins=bins, labels=labels, right=False)
        
        # Count by age group and gender
        age_gender = filtered_df.groupby(['AgeGroup', 'Gender']).size().unstack().fillna(0)
        
        # Create grouped bar chart
        age_gender_melted = age_gender.reset_index().melt(id_vars='AgeGroup', value_vars=age_gender.columns, 
                                                          var_name='Gender', value_name='Count')
        
        fig = px.bar(
            age_gender_melted,
            x='AgeGroup',
            y='Count',
            color='Gender',
            title='Age Distribution by Gender',
            barmode='group',
            color_discrete_map=GENDER_COLORS
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='Age Group',
            yaxis_title='Number of Employees'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_header("Years of Service")
        
        # Create service bins
        bins = [0, 2, 5, 10, 15, 30]
        labels = ['0-2', '3-5', '6-10', '11-15', '16+']
        filtered_df['ServiceGroup'] = pd.cut(filtered_df['YearsAtCompany'], bins=bins, labels=labels, right=False)
        
        # Count by service group
        service_counts = filtered_df['ServiceGroup'].value_counts().reset_index()
        service_counts.columns = ['Years of Service', 'Count']
        
        # Sort by years
        service_counts['Years of Service'] = pd.Categorical(service_counts['Years of Service'], 
                                                            categories=labels, ordered=True)
        service_counts = service_counts.sort_values('Years of Service')
        
        fig = px.bar(
            service_counts,
            x='Years of Service',
            y='Count',
            title='Employee Tenure Distribution',
            text='Count',
            color_discrete_sequence=[PRIMARY_COLOR]
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='',
            yaxis_title='Number of Employees'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Job roles distribution
    st.markdown("---")
    section_header("Job Roles by Department")
    
    # Count by job role and department
    role_dept = filtered_df.groupby(['Department', 'JobRole']).size().unstack().fillna(0)
    role_dept_melted = role_dept.reset_index().melt(id_vars='Department', value_vars=role_dept.columns, 
                                                   var_name='JobRole', value_name='Count')
    
    # Create stacked bar chart
    fig = px.bar(
        role_dept_melted,
        x='Department',
        y='Count',
        color='JobRole',
        title='Job Roles Distribution by Department',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        xaxis_title='',
        yaxis_title='Number of Employees',
        legend=dict(title='Job Role')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Performance tab
with tabs[2]:
    st.subheader("Performance Analysis")
    
    # Performance distribution
    col1, col2 = st.columns(2)
    
    with col1:
        section_header("Performance Rating Distribution")
        
        # Count by performance rating
        perf_counts = filtered_df['PerformanceRating'].value_counts().reset_index()
        perf_counts.columns = ['Rating', 'Count']
        
        # Add labels
        perf_labels = {
            1: "Poor", 
            2: "Below Average", 
            3: "Average", 
            4: "Good", 
            5: "Excellent"
        }
        perf_counts['Label'] = perf_counts['Rating'].map(perf_labels)
        
        # Sort by rating
        perf_counts = perf_counts.sort_values('Rating')
        
        # Create bar chart with performance colors
        colors = [PERFORMANCE_COLORS[rating] for rating in perf_counts['Rating']]
        
        fig = px.bar(
            perf_counts,
            x='Rating',
            y='Count',
            title='Performance Rating Distribution',
            text='Count',
            labels={'Rating': 'Performance Rating', 'Count': 'Number of Employees'}
        )
        
        # Update bar colors
        fig.update_traces(marker_color=colors)
        
        # Add annotations for labels
        for i, row in perf_counts.iterrows():
            fig.add_annotation(
                x=row['Rating'],
                y=row['Count'],
                text=row['Label'],
                showarrow=False,
                yshift=10,
                font=dict(color='white', size=10)
            )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='Performance Rating',
            yaxis_title='Number of Employees'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_header("Performance by Job Role")
        
        # Calculate average performance by job role
        perf_by_role = filtered_df.groupby('JobRole')['PerformanceRating'].mean().reset_index()
        perf_by_role = perf_by_role.sort_values('PerformanceRating', ascending=False)
        
        # Create horizontal bar chart
        fig = px.bar(
            perf_by_role,
            y='JobRole',
            x='PerformanceRating',
            orientation='h',
            title='Average Performance Rating by Job Role',
            text=perf_by_role['PerformanceRating'].round(1),
            color='PerformanceRating'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='Average Performance Rating (1-5)',
            yaxis_title='',
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Satisfaction vs Years at Company
    st.markdown("---")
    section_header("Job Satisfaction & Tenure")
    
    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='YearsAtCompany',
        y='JobSatisfaction',
        color='PerformanceRating',
        size='Salary',
        hover_data=['Department', 'JobRole', 'Gender'],
        title='Job Satisfaction vs Years at Company'
    )
    
    # Add trendline
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        xaxis_title='Years at Company',
        yaxis_title='Job Satisfaction (1-4)',
        coloraxis=dict(colorbar=dict(title='Performance Rating'))
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Attrition tab
with tabs[3]:
    st.subheader("Attrition Analysis")
    
    # Overview KPIs
    col1, col2, col3 = st.columns(3)
    
    # Calculate attrition metrics
    total_employees = len(filtered_df)
    attrition_count = filtered_df[filtered_df['Attrition'] == 'Yes'].shape[0]
    attrition_rate = round((attrition_count / total_employees) * 100, 1) if total_employees > 0 else 0
    
    with col1:
        styled_card("Attrition Rate", f"{attrition_rate}%", "🔄")
    
    with col2:
        styled_card("Employees Left", f"{attrition_count:,}", "👋")
    
    with col3:
        styled_card("Retained", f"{total_employees - attrition_count:,}", "🏆")
    
    # Attrition charts
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        section_header("Attrition by Department")
        
        # Calculate attrition by department
        dept_attrition = filtered_df.groupby(['Department', 'Attrition']).size().unstack().fillna(0)
        
        if 'Yes' in dept_attrition.columns:
            dept_attrition['Total'] = dept_attrition.sum(axis=1)
            dept_attrition['AttritionRate'] = dept_attrition['Yes'] / dept_attrition['Total'] * 100
            
            # Sort by attrition rate
            dept_attrition = dept_attrition.sort_values('AttritionRate', ascending=False)
            
            # Create bar chart
            dept_attrition_df = dept_attrition.reset_index()
            
            colors = [DEPARTMENT_COLORS.get(dept, PRIMARY_COLOR) for dept in dept_attrition_df['Department']]
            
            fig = px.bar(
                dept_attrition_df,
                x='Department',
                y='AttritionRate',
                title='Attrition Rate by Department (%)',
                text=dept_attrition_df['AttritionRate'].round(1).astype(str) + '%',
                color='Department',
                color_discrete_map=DEPARTMENT_COLORS
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_COLOR),
                xaxis_title='',
                yaxis_title='Attrition Rate (%)',
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_header("Attrition by Job Role")
        
        # Calculate attrition by job role
        role_attrition = filtered_df.groupby(['JobRole', 'Attrition']).size().unstack().fillna(0)
        
        if 'Yes' in role_attrition.columns:
            role_attrition['Total'] = role_attrition.sum(axis=1)
            role_attrition['AttritionRate'] = role_attrition['Yes'] / role_attrition['Total'] * 100
            
            # Sort by attrition rate
            role_attrition = role_attrition.sort_values('AttritionRate', ascending=False)
            
            # Create bar chart
            role_attrition_df = role_attrition.reset_index()
            
            fig = px.bar(
                role_attrition_df,
                x='JobRole',
                y='AttritionRate',
                title='Attrition Rate by Job Role (%)',
                text=role_attrition_df['AttritionRate'].round(1).astype(str) + '%',
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_COLOR),
                xaxis_title='',
                yaxis_title='Attrition Rate (%)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Attrition by satisfaction and performance
    st.markdown("---")
    section_header("Attrition Factors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Attrition by job satisfaction
        att_by_sat = filtered_df.groupby(['JobSatisfaction', 'Attrition']).size().unstack().fillna(0)
        
        if 'Yes' in att_by_sat.columns:
            att_by_sat['Total'] = att_by_sat.sum(axis=1)
            att_by_sat['AttritionRate'] = att_by_sat['Yes'] / att_by_sat['Total'] * 100
            
            # Create line chart
            att_by_sat_df = att_by_sat.reset_index()
            
            fig = px.line(
                att_by_sat_df,
                x='JobSatisfaction',
                y='AttritionRate',
                title='Attrition Rate by Job Satisfaction',
                markers=True,
                color_discrete_sequence=[HIGHLIGHT_COLOR]
            )
            
            # Add annotations
            for i, row in att_by_sat_df.iterrows():
                fig.add_annotation(
                    x=row['JobSatisfaction'],
                    y=row['AttritionRate'],
                    text=f"{row['AttritionRate']:.1f}%",
                    showarrow=False,
                    yshift=10,
                    font=dict(color=TEXT_COLOR)
                )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_COLOR),
                xaxis_title='Job Satisfaction (1-4)',
                yaxis_title='Attrition Rate (%)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Attrition by performance
        att_by_perf = filtered_df.groupby(['PerformanceRating', 'Attrition']).size().unstack().fillna(0)
        
        if 'Yes' in att_by_perf.columns:
            att_by_perf['Total'] = att_by_perf.sum(axis=1)
            att_by_perf['AttritionRate'] = att_by_perf['Yes'] / att_by_perf['Total'] * 100
            
            # Create line chart
            att_by_perf_df = att_by_perf.reset_index()
            
            fig = px.line(
                att_by_perf_df,
                x='PerformanceRating',
                y='AttritionRate',
                title='Attrition Rate by Performance Rating',
                markers=True,
                color_discrete_sequence=[HIGHLIGHT_COLOR]
            )
            
            # Add annotations
            for i, row in att_by_perf_df.iterrows():
                fig.add_annotation(
                    x=row['PerformanceRating'],
                    y=row['AttritionRate'],
                    text=f"{row['AttritionRate']:.1f}%",
                    showarrow=False,
                    yshift=10,
                    font=dict(color=TEXT_COLOR)
                )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_COLOR),
                xaxis_title='Performance Rating (1-5)',
                yaxis_title='Attrition Rate (%)'
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Compensation tab
with tabs[4]:
    st.subheader("Compensation Analysis")
    
    # Overview KPIs
    col1, col2, col3 = st.columns(3)
    
    # Calculate salary metrics
    avg_salary = int(filtered_df['Salary'].mean())
    median_salary = int(filtered_df['Salary'].median())
    salary_range = f"${int(filtered_df['Salary'].min()):,} - ${int(filtered_df['Salary'].max()):,}"
    
    with col1:
        styled_card("Average Salary", f"${avg_salary:,}", "💰")
    
    with col2:
        styled_card("Median Salary", f"${median_salary:,}", "📊")
    
    with col3:
        styled_card("Salary Range", salary_range, "📈")
    
    # Salary by department and job role
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        section_header("Salary by Department")
        
        # Calculate average salary by department
        dept_salary = filtered_df.groupby('Department')['Salary'].mean().reset_index()
        dept_salary = dept_salary.sort_values('Salary', ascending=False)
        
        fig = px.bar(
            dept_salary,
            x='Department',
            y='Salary',
            title='Average Salary by Department',
            text=dept_salary['Salary'].apply(lambda x: f"${int(x):,}"),
            color='Department',
            color_discrete_map=DEPARTMENT_COLORS
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='',
            yaxis_title='Average Salary ($)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_header("Salary by Job Role")
        
        # Calculate average salary by job role
        role_salary = filtered_df.groupby('JobRole')['Salary'].mean().reset_index()
        role_salary = role_salary.sort_values('Salary', ascending=False)
        
        fig = px.bar(
            role_salary,
            x='JobRole',
            y='Salary',
            title='Average Salary by Job Role',
            text=role_salary['Salary'].apply(lambda x: f"${int(x):,}"),
            color_discrete_sequence=[PRIMARY_COLOR]
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='',
            yaxis_title='Average Salary ($)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Salary correlation
    st.markdown("---")
    section_header("Salary Correlations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary vs Years at Company
        fig = px.scatter(
            filtered_df,
            x='YearsAtCompany',
            y='Salary',
            color='Department',
            size='PerformanceRating',
            hover_data=['JobRole', 'Gender', 'Age'],
            title='Salary vs Years at Company',
            color_discrete_map=DEPARTMENT_COLORS
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='Years at Company',
            yaxis_title='Salary ($)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Salary vs Performance
        fig = px.box(
            filtered_df,
            x='PerformanceRating',
            y='Salary',
            color='PerformanceRating',
            title='Salary Distribution by Performance Rating'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_COLOR),
            xaxis_title='Performance Rating',
            yaxis_title='Salary ($)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Gender pay gap
    st.markdown("---")
    section_header("Gender Pay Analysis")
    
    # Calculate average salary by department and gender
    gender_dept_salary = filtered_df.groupby(['Department', 'Gender'])['Salary'].mean().reset_index()
    
    fig = px.bar(
        gender_dept_salary,
        x='Department',
        y='Salary',
        color='Gender',
        barmode='group',
        title='Average Salary by Department and Gender',
        color_discrete_map=GENDER_COLORS
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        xaxis_title='',
        yaxis_title='Average Salary ($)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: {MUTED_TEXT_COLOR}; padding: 20px 0;">
        <p>HR Analytics Dashboard | Created with Streamlit</p>
    </div>
    """, 
    unsafe_allow_html=True
)