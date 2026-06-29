import pandas as pd
import streamlit as st
import plotly.express as px


# Perform safe division with zero and null protection.
def safe_divide(numerator, denominator, scale=1.0):
    if denominator is None or denominator == 0 or (isinstance(denominator, float) and pd.isna(denominator)):
        return 0.0
    return float(numerator) * scale / float(denominator)


# Calculate dashboard KPI values from applications and visitor events.
def calculate_kpis(applications, events):
    total_visitors = int(events[events['event_type'] == 'visitor']['visitor_id'].nunique())
    total_applications = int(applications.shape[0])
    successful_applications = int(applications[applications['status'] == 'Hired'].shape[0])
    rejected_applications = int(applications[applications['status'] == 'Rejected'].shape[0])
    conversion_rate = safe_divide(successful_applications, total_applications, 100)
    avg_applications = safe_divide(total_applications, applications['job_id'].nunique())

    return {
        'total_visitors': total_visitors,
        'total_applications': total_applications,
        'successful_applications': successful_applications,
        'rejected_applications': rejected_applications,
        'conversion_rate': conversion_rate,
        'avg_applications': avg_applications,
    }


# Build a Plotly pie chart summarizing application status distribution.
def build_status_chart(applications):
    if applications.empty:
        return None

    status_counts = applications['status'].fillna('Unknown').value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    return px.pie(
        status_counts,
        names='Status',
        values='Count',
        title='Application Status Distribution',
        hole=0.4,
    )


# Render the Conversion Dashboard page with KPIs and status chart.
def render_conversion_dashboard(data):
    st.header('Conversion Dashboard')
    applications = data['applications']
    events = data['events']

    if applications.empty and events.empty:
        st.warning('No application or event data is available for the selected filters.')
        return

    metrics = calculate_kpis(applications, events)
    cols = st.columns(3)
    cols[0].metric('Total Visitors', metrics['total_visitors'])
    cols[0].metric('Total Applications', metrics['total_applications'])
    cols[1].metric('Successful Applications', metrics['successful_applications'])
    cols[1].metric('Rejected Applications', metrics['rejected_applications'])
    cols[2].metric('Conversion Rate %', f"{metrics['conversion_rate']:.1f}%")
    cols[2].metric('Average Applications per Job', f"{metrics['avg_applications']:.1f}")

    st.markdown('---')
    chart = build_status_chart(applications)
    if chart is not None:
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.warning('No application status distribution can be shown for the current data set.')
