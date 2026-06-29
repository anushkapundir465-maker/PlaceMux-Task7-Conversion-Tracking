import streamlit as st
import pandas as pd
from datetime import datetime
from pages_logic import (
    analytics,
    application_flow,
    conversion_dashboard,
    conversion_funnel,
    tracking_plan,
)
from utils.data_manager import load_all_data, apply_filters

st.set_page_config(
    page_title='PlaceMux Conversion Analytics',
    page_icon='📈',
    layout='wide',
)

PAGE_MAP = {
    'Conversion Dashboard': conversion_dashboard.render_conversion_dashboard,
    'Application Flow': application_flow.render_application_flow,
    'Conversion Funnel': conversion_funnel.render_conversion_funnel,
    'Analytics': analytics.render_analytics,
    'Tracking Plan': tracking_plan.render_tracking_plan,
}


# Build sidebar selectors for company, job, date range, and search term.
# The sidebar filters are applied across applications, events, and conversions.
def build_sidebar_filters(data):
    st.sidebar.header('Filters')
    companies = ['All Companies'] + sorted(
        data['companies']['name'].dropna().astype(str).unique().tolist()
    )
    jobs = ['All Jobs'] + sorted(
        data['jobs']['title'].dropna().astype(str).unique().tolist()
    )
    selected_company = st.sidebar.selectbox('Company', companies)
    selected_job = st.sidebar.selectbox('Job', jobs)

    min_date = data['applications']['application_date'].min()
    max_date = data['applications']['application_date'].max()
    if pd.isna(min_date) or pd.isna(max_date):
        min_date = max_date = datetime.now()

    start_date = min_date.date() if hasattr(min_date, 'date') else datetime.now().date()
    end_date = max_date.date() if hasattr(max_date, 'date') else datetime.now().date()

    date_range = st.sidebar.date_input(
        'Date range',
        value=(start_date, end_date),
        min_value=start_date,
        max_value=end_date,
        help='Filter events and applications by date.',
    )
    if isinstance(date_range, datetime):
        date_range = (date_range.date(), date_range.date())

    search_term = st.sidebar.text_input('Search', placeholder='Search job, company, or candidate')
    st.sidebar.markdown('---')
    st.sidebar.markdown(
        'Built for data analysts and growth teams to explore pay-per-application activity.'
    )
    return selected_company, selected_job, date_range, search_term


# Main entry point for the Streamlit app.
# Loads data, applies sidebar filters, and routes to the selected page.
def main():
    import pandas as pd
    from datetime import datetime

    st.title('PlaceMux Phase 2 – Pay-per-Application Flow')
    st.markdown(
        'Use the sidebar to explore conversion metrics, application workflows, funnel performance, analytics, and tracking definitions.'
    )

    data, warnings = load_all_data()

    if warnings:
        for message in warnings:
            st.sidebar.warning(message)

    selected_company, selected_job, date_range, search_term = build_sidebar_filters(data)

    filtered_data = apply_filters(
        data,
        company=selected_company if selected_company != 'All Companies' else None,
        job=selected_job if selected_job != 'All Jobs' else None,
        date_range=tuple(date_range) if isinstance(date_range, tuple) and len(date_range) == 2 else None,
        search_term=search_term.strip() or None,
    )

    PAGE_MAP[st.sidebar.radio('Navigation', list(PAGE_MAP.keys()), index=0)](filtered_data)


if __name__ == '__main__':
    main()
