import streamlit as st


def build_flow_metrics(applications, events):
    return {
        'Visitors': int(events[events['event_type'] == 'visitor']['visitor_id'].nunique()),
        'Job Views': int(events[events['event_type'] == 'job_view'].shape[0]),
        'Apply Clicks': int(events[events['event_type'] == 'apply_click'].shape[0]),
        'Applications Submitted': int(applications.shape[0]),
        'Shortlisted': int(applications[applications['status'] == 'Shortlisted'].shape[0]),
        'Hired': int(applications[applications['status'] == 'Hired'].shape[0]),
    }


def render_application_flow(data):
    st.header('Application Flow')
    applications = data['applications']
    events = data['events']

    if applications.empty and events.empty:
        st.warning('No application or event records are available for this filter selection.')
        return

    metrics = build_flow_metrics(applications, events)
    cols = st.columns(3)
    cols[0].metric('Visitor Count', metrics['Visitors'])
    cols[0].metric('Job Views', metrics['Job Views'])
    cols[1].metric('Apply Clicks', metrics['Apply Clicks'])
    cols[1].metric('Applications Submitted', metrics['Applications Submitted'])
    cols[2].metric('Shortlisted', metrics['Shortlisted'])
    cols[2].metric('Hired', metrics['Hired'])

    st.markdown('---')
    st.subheader('Filtered Application Timeline')
    if not applications.empty:
        st.dataframe(
            applications[
                ['application_id', 'application_date', 'company_name', 'job_title', 'candidate_name', 'status', 'source', 'applied_from']
            ].sort_values(by='application_date', ascending=False),
            use_container_width=True,
        )
    else:
        st.info('No applications match the current filters.')

    st.markdown('---')
    st.subheader('Event Journey')
    if not events.empty:
        st.dataframe(
            events[
                ['event_time', 'session_id', 'visitor_id', 'event_type', 'page_url', 'job_id', 'company_id']
            ].sort_values(by='event_time', ascending=False),
            use_container_width=True,
        )
    else:
        st.info('No events match the current filters.')

    if not applications.empty:
        st.download_button(
            'Download filtered applications CSV',
            applications.to_csv(index=False).encode('utf-8'),
            file_name='filtered_applications.csv',
            mime='text/csv',
        )
