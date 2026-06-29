import pandas as pd
import plotly.express as px
import streamlit as st


def render_analytics(data):
    st.header('Analytics')
    applications = data['applications']

    if applications.empty:
        st.warning('No application analytics are available for the selected filters.')
        return

    daily = (
        applications.dropna(subset=['application_date'])
        .groupby(applications['application_date'].dt.date)['application_id']
        .count()
        .rename('applications')
        .reset_index()
    )
    if daily.empty:
        st.warning('There is no daily application data to display.')
        return

    hired_daily = (
        applications[applications['status'] == 'Hired']
        .groupby(applications['application_date'].dt.date)['application_id']
        .count()
        .rename('hired_count')
    )
    daily = daily.merge(hired_daily, on='application_date', how='left').fillna(0)
    daily['conversion_rate'] = (daily['hired_count'] / daily['applications'].replace(0, pd.NA) * 100).fillna(0)

    fig_daily = px.line(
        daily,
        x='application_date',
        y='conversion_rate',
        title='Daily Conversion Rate Trend',
        markers=True,
    )
    fig_daily.update_xaxes(title_text='Date')
    fig_daily.update_yaxes(title_text='Conversion Rate (%)')

    company_volume = (
        applications.groupby('company_name')['application_id']
        .count()
        .rename('applications')
        .reset_index()
        .sort_values(by='applications', ascending=False)
    )

    job_volume = (
        applications.groupby('job_title')['application_id']
        .count()
        .rename('applications')
        .reset_index()
        .sort_values(by='applications', ascending=False)
        .head(10)
    )

    company_rate = (
        applications.groupby('company_name')['status']
        .apply(lambda x: (x == 'Hired').sum() / x.count() if x.count() else 0)
        .rename('hiring_success_rate')
        .reset_index()
    )
    company_rate['hiring_success_rate'] = company_rate['hiring_success_rate'] * 100
    company_rate = company_rate.sort_values(by='hiring_success_rate', ascending=False).head(10)

    cols = st.columns(2)
    cols[0].plotly_chart(fig_daily, use_container_width=True)
    if not company_volume.empty:
        cols[1].plotly_chart(
            px.bar(
                company_volume,
                x='applications',
                y='company_name',
                orientation='h',
                title='Applications by Company',
            ).update_layout(yaxis_title='Company', xaxis_title='Applications'),
            use_container_width=True,
        )

    st.markdown('---')
    cols2 = st.columns(2)
    cols2[0].plotly_chart(
        px.bar(
            job_volume,
            x='applications',
            y='job_title',
            orientation='h',
            title='Top 10 Jobs by Applications',
        ).update_layout(yaxis_title='Job Title', xaxis_title='Applications', margin=dict(l=120, r=20, t=40, b=40)),
        use_container_width=True,
    )
    cols2[1].plotly_chart(
        px.bar(
            company_rate,
            x='hiring_success_rate',
            y='company_name',
            orientation='h',
            title='Hiring Success Rate by Company',
            labels={'hiring_success_rate': 'Hiring Success Rate (%)', 'company_name': 'Company'},
        ).update_layout(xaxis_tickformat='.1f'),
        use_container_width=True,
    )

    st.markdown('---')
    conversion_by_company = (
        applications.groupby('company_name')['status']
        .apply(lambda x: (x == 'Hired').sum() / x.count() if x.count() else 0)
        .rename('conversion_rate')
        .reset_index()
    )
    conversion_by_company['conversion_rate'] = conversion_by_company['conversion_rate'] * 100

    if not conversion_by_company.empty:
        st.plotly_chart(
            px.bar(
                conversion_by_company.sort_values(by='conversion_rate', ascending=False),
                x='conversion_rate',
                y='company_name',
                orientation='h',
                title='Conversion Rate by Company',
                labels={'conversion_rate': 'Conversion Rate (%)', 'company_name': 'Company'},
            ).update_layout(xaxis_tickformat='.1f'),
            use_container_width=True,
        )
